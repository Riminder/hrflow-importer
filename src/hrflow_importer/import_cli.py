import os
import time
import typing
import typer

from hrflow_importer.importer.worker import send_batch_to_hrflow
from hrflow_importer.utils.config.config import config #TODO improve module naming for import

from hrflow import Hrflow

PIPELINES_LOGS_FILE = "{}/importer_logs.txt".format(config.STORAGE_DIRECTORY_PATH)


cli = typer.Typer()


def display_results(results: typing.Counter) -> None:
    total = sum(results.values())
    if total > 0:
        typer.echo("\t\t{:<40} {:>5}".format("total", total))
        for status, count in results.items():
            typer.echo(
                "\t\t" + "{:<40} {:>5} ({:.0%})".format(status, count, count / total)
            )


# ---- CLI ----
# The functions defined in this section are wrappers around the main function
# send_batch_to_hrflow allowing them to be called directly from the terminal as a CLI
# executable/script.


@cli.command()
def local(max_workers: int = typer.Option(None)):
    """Parse files in ./app_data/files."""
    section_name = "Worker Parameters"
    seperator = "=" * ((100 - len(section_name))//2)
    typer.echo(seperator + section_name + seperator)
    multiprocess = int(typer.prompt("Use multiprocessing [1: yes, 0: no]"))
    if multiprocess:
        sleep_period = 6 #default value
        typer.echo("Proceeding with multiprocessing.")
    else:
        typer.echo("Proceeding without multiprocessing. Select sleep time between API calls.")
        sleep_period = int(typer.prompt("Sleep period (in seconds)"))

    section_name = "HrFlow API Config"
    seperator = "=" * ((100 - len(section_name))//2)
    typer.echo(seperator + section_name + seperator)
    api_secret = typer.prompt("API Secret Key ")  
    team = typer.prompt("Team Name ")
    source_key = typer.prompt("Source Key ")
    api_user = typer.prompt("API User Email ") 

    client = Hrflow(api_secret=api_secret, api_user=api_user)

    start = time.time()

    typer.echo("=" * 100)
    typer.echo("[Import Command] Started")

    typer.echo("[Import Command][Stats]")
    filename_list = os.listdir(os.path.join(config.STORAGE_DIRECTORY_PATH, config.LOCAL_FILES_FOLDER)) #TODO prompt through cli parameters
    file_reference_list = filename_list #TODO integrate reference generation in FileHandler internal logic
    n_files = len(filename_list)
    typer.echo("\t\t n_files={}".format(n_files))

    typer.echo("[Import Command][Importing]")
    typer.echo(
        "\t\t Imorting files to \n\t\t\tteam={} \n\t\t\tsource={}".format(
            team, source_key
        )
    )
    #TODO refactor this part
    parsing_results = send_batch_to_hrflow(client,
                            source_key,
                            filename_list,
                            file_reference_list,
                            multiprocess,
                            sleep_period
                        )
    #parsing_results = send_batch_to_hrflow(client, source_key, filename_list, file_reference_list, max_workers)

    typer.echo("[Import Command][Parsing] Results")
    display_results(parsing_results)

    typer.echo("[Import Command] Finished in {:.1f}s".format(time.time() - start))
    typer.echo("=" * 100)

if __name__ == "__main__":
    cli()
