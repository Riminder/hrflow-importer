<p align="center">
  <a href="https://hrflow.ai">
    <img alt="hrflow" src="https://img.riminder.net/logo-hrflow.svg" width="120" />
  </a>
</p>
<h1 align="center">
  HrFlow Importer
</h1>

<!-- ![GitHub Repo stars](https://img.shields.io/github/stars/Riminder/hrflow-connectors?style=social) ![](https://img.shields.io/github/v/release/Riminder/hrflow-connectors) ![](https://img.shields.io/github/license/Riminder/hrflow-connectors) -->


<!-- <p align="center">
  <a href="https://hrflow.ai">
    <img alt="hrflow" src="https://hrflow-ai.imgix.net/corporate.svg"/>
  </a>
</p> -->

<br/>

## Description
A python package for batch import of resume attachments to be parsed in HrFlow.

`hrflow-importer` is an open-source project created by **HrFlow.ai** 
to seamlessly import resume attachments from local folder into HrFlow.

## 🪄 Quickstart
### What I can do?
With Hrflow Importer, you can **import** a batch of resume attachments in a local directory into HrFlow.ai to be **parsed**, using a command line directly from your terminal.

### How to use HrFlow Importer ?
**Prerequisites**
* [✨ Create a Workspace](https://hrflow.ai/signup/)
* [🔑 Get your API Key](https://developers.hrflow.ai/docs/api-authentification)
* [Create a Source](https://developers.hrflow.ai/reference/the-source-object) 

1. **`pip install hrflow-importer`**
2. **setup your .env file**. You can do this by running command:
```bash
cat env.example >> .env 
```
And then fill the values in the **.env** file accordingly.
3. Run the command 
```bash
hrflow_import
```
and fill the prompted values. 


🐇 **TADA! You should see a progress bar for the upload.**


## 🚀 Environment

**To find the list of dependencies, you can look at the [`pyproject.toml`](pyproject.toml) file**

## :woman_technologist: Contributions

Please feel free to contribute to the quality of this content by
submitting PRs for improvements to code, architecture, etc. 

Any contributions you make to this effort are of course greatly 
appreciated.

👉 **To find out more about how to proceed, the rules and conventions to follow, read carefully [`CONTRIBUTING.md`](CONTRIBUTING.md).**

## 🔗 Resources
* Our Developers documentation : https://developers.hrflow.ai/
* Our API list (Parsing, Revealing, Embedding, Searching, Scoring, Reasoning) : https://www.hrflow.ai/api
* Our cool demos labs : https://labs.hrflow.ai

## :page_with_curl: License

See the [`LICENSE`](LICENSE) file for licensing information.


