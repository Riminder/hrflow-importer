from enum import Enum
import os
from typing import Callable, Union


class EnvironmentVariable:
    def __init__(
        self,
        variable_name: str = None,
        *,
        prefix: str = "XX",
        default: Union[str, bool, int, float] = None,
        formatter: Callable = lambda x: x,
        validator: Callable = lambda x: None
    ):
        self.variable_name = variable_name
        self.default = default
        self.prefix = prefix
        self.formatter = formatter
        self.validator = validator

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.attribute_name)

    def __set__(self, instance, value):
        instance.__dict__[self.attribute_name] = value

    def __set_name__(self, owner, name):
        self.attribute_name = "{}_{}".format(self.prefix, name)
        if self.variable_name is None:
            self.variable_name = name

    def load_from_env(self, instance):
        value_from_environment = os.getenv(self.variable_name)
        if value_from_environment is not None:
            try:
                self.validator(value_from_environment)
                formatted = self.formatter(value_from_environment)
                instance.__dict__[self.attribute_name] = formatted
            except ValueError as e:
                raise ValueError(
                    "Error while loading {}('{}') : {}".format(
                        self.__class__.__name__, self.variable_name, " ".join(e.args)
                    )
                )
        elif self.default is not None:
            instance.__dict__[self.attribute_name] = self.default
        else:
            raise ValueError(
                "No value nor default set for {}('{}')".format(
                    self.__class__.__name__, self.variable_name
                )
            )


class IntEnvironmentVariable(EnvironmentVariable):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs, formatter=int)


class FloatEnvironmentVariable(EnvironmentVariable):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs, formatter=float)


class BoolEnvironmentVariable(EnvironmentVariable):
    def __init__(self, *args, **kwargs):
        return super().__init__(
            *args, **kwargs, formatter=BoolEnvironmentVariable.cast_to_bool
        )

    @staticmethod
    def cast_to_bool(value: str) -> bool:
        if isinstance(value, str):
            if value.lower().strip() == "true":
                return True
            elif value.lower().strip() == "false":
                return False
        raise ValueError(
            "invalid value provided '{}'. Value should verify `value.lower().strip() in ['true', 'false']`".format(
                value
            )
        )


class OptionsEnvironmentVariable(EnvironmentVariable):
    def __init__(self, *args, options=Enum, **kwargs):
        return super().__init__(
            *args,
            **kwargs,
            formatter=OptionsEnvironmentVariable.cast_to_enum_member(options),
            validator=OptionsEnvironmentVariable.options_validator(options)
        )

    @staticmethod
    def options_validator(options: Enum):
        def validator(value: str):
            try:
                options[value]
            except KeyError:
                raise ValueError(
                    "invalid value provided '{}'. Value should be one of (case-sensitive) {}".format(
                        value, [option.name for option in options]
                    )
                )

        return validator

    @staticmethod
    def cast_to_enum_member(options: Enum):
        def enum_member(value: str):
            return options[value]

        return enum_member


class BaseConfig:
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)
        for attribute in type(instance).__dict__.values():
            if isinstance(attribute, EnvironmentVariable):
                attribute.load_from_env(instance)
        return instance


class Config(BaseConfig):
    STORAGE_DIRECTORY_PATH = EnvironmentVariable()
    LOCAL_FILES_FOLDER = EnvironmentVariable()
    LOCAL_FAILURES_FOLDER = EnvironmentVariable()

config = Config()
