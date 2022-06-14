"""Custom logging module"""

import inspect
import logging
import os
import re
import shutil
import sys
import time
from datetime import datetime

import colorama
import coloredlogs
import pyinputplus as py_option
from colorama import Back, Cursor, Fore, Style

from .config import settings


def __getattr__(name):
    return getattr(logging, name)


class NameFilter(logging.Filter):
    """Class to add called variable to logger"""

    def __init__(self) -> None:
        super().__init__()
        self.name = "NameFilter"

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Console filter
        :param record: Record to emit
        :type record: logging.LogRecord
        :return: Record
        :rtype: bool
        """
        caller_exist = getattr(record, "caller", "")
        if not caller_exist:
            record.caller = ""
        record.name = fix_mod_path(record.name)
        if record.name != record.module:
            record.funcName = f"{record.module}.{record.funcName}"
        if default_color:
            spacers = (spacer_color + spacer) * (58 - len(record.funcName))
        else:
            spacers = ""
        record.filefuncName = record.funcName
        record.msg = str(record.msg)
        record.filemessage = re.sub(r"[^a-zA-Z']\[...", "", record.msg)
        record.funcName = f"{record.funcName} " f"{spacers}"

        fixed_text = record.msg
        file_text = record.msg
        curr_bold = ""
        curr_faint = ""
        style_tag = {"c": "fore", "s": "style", "b": "back"}
        each_attrib_count = 0
        for style_search in style_tag:
            style_regex = (r"%" + style_search + r"\.(\w*)%(.*?)%" +
                           style_search + r"%")
            add_attrib = re.findall(style_regex, record.msg)
            if add_attrib:
                for each_attrib in add_attrib:
                    attrib_add = each_attrib[0]
                    if (attrib_add.upper()
                            not in valid_attrib[each_attrib_count]):
                        print(f"Invalid option specified - {attrib_add}")
                        continue
                    fixed_text = re.sub(
                        style_regex,
                        text_color(
                            each_attrib[1], attrib_add,
                            style_tag[style_search]
                            ),
                        fixed_text,
                        count=1,
                        )
                    file_text = re.sub(
                        style_regex,
                        each_attrib[1],
                        file_text,
                        count=1
                        )
                    if not default_color:
                        fixed_text = file_text
            each_attrib_count += 1
            if style_search == "s":
                curr_bold = error_color_format.get(
                    record.levelname.lower()
                    ).get("bright", "")
                if curr_bold:
                    curr_bold = Style.BRIGHT
                curr_faint = error_color_format.get(
                    record.levelname.lower()
                    ).get("faint", "")
                if curr_faint:
                    curr_faint = Style.DIM

        curr_color = error_color_format.get(record.levelname.lower()).get(
            "color", ""
            )
        if curr_color.isnumeric():
            curr_color = "\033[" + curr_color + "m"
        else:
            curr_color = getattr(colorama.Fore, curr_color.upper(), "")

        curr_back = error_color_format.get(record.levelname.lower()).get(
            "background", ""
            )
        if curr_back.isnumeric():
            curr_back = "\033[" + curr_back
        else:
            curr_back = getattr(colorama.Back, curr_back.upper(), "")

        curr_reset = curr_back + curr_color + curr_faint + curr_bold
        reset_text = curr_reset + fixed_text.replace(Fore.RESET, curr_color)
        reset_text = reset_text.replace(Back.RESET, curr_back)
        reset_text = reset_text.replace(
            Style.RESET_ALL,
            curr_faint + curr_bold
            )
        record.msg = reset_text + curr_reset
        record.filemessage = file_text
        return True


default_spacer = ""
default_spacer_color = "LIGHTBLACK_EX"

try:
    spacer = settings.spacer
except AttributeError:
    logging.warning(
        f"'spacer' missing in settings using "
        f"'{default_spacer}'"
        )
    spacer = default_spacer

try:
    spacer_color = settings.spacer_color
except AttributeError:
    logging.warning(
        f"'spacer_color' missing in settings using "
        f"'{default_spacer_color.split('.')[-1]}'"
        )
    spacer_color = default_spacer_color

spacer_color = getattr(colorama.Fore, spacer_color.upper())

base_log = logging.getLogger(__file__)
base_log.addFilter(NameFilter())

valid_colors = []
for get_valid_colors in dir(Fore):
    if get_valid_colors.isupper():
        valid_colors.append(get_valid_colors)

valid_styles = []
for get_valid_styles in dir(Style):
    if get_valid_styles.isupper():
        valid_styles.append(get_valid_styles)

valid_back = []
for get_valid_back in dir(Back):
    if get_valid_back.isupper():
        valid_back.append(get_valid_back)

valid_cursor = []
for get_valid_cursor in dir(Cursor):
    if get_valid_cursor.isupper():
        valid_cursor.append(get_valid_cursor)

valid_attrib = [valid_colors, valid_styles, valid_back]

total_reset = Fore.RESET + Style.RESET_ALL + Back.RESET

file_log_format = (
    r"%(asctime)s.%(msecs)03d,%(filefuncName)s,%(levelname)s,%(filemessage)s")
console_log_format = (r"%(asctime)s.%(msecs)03d %(name)-20s %(funcName)-60s " +
                      " %(levelname)-10s %(message)-s")
caller_log_format = (r"%(asctime)s.%(msecs)03d %(name)-20s %(caller)-60s  "
                     r"%(levelname)-10s "
                     r"%(message)-s")
caller_color_format = coloredlogs.DEFAULT_FIELD_STYLES
caller_color_format.update(
    {
        "caller": {
            "color": 133
            },
        "varname": {
            "color": "red"
            },
        "levelname": {
            "color": 48
            },
        }
    )

error_color_format = coloredlogs.DEFAULT_LEVEL_STYLES
error_color_format.update(
    {
        "error": {
            "color": "black",
            "background": "red"
            },
        "info": {
            "color": "blue"
            },
        "warning": {
            "color": "red"
            },
        }
    )

default_log_path = "C:\\Logs"
default_level = "INFO"
default_file_level = "INFO"
default_auto_create = False
default_log_to_file = False
default_log_ext = "log"
default_color = True

try:
    default_log_path = settings.logging_path
except AttributeError:
    base_log.critical(
        f"'logging_path' missing in settings using {default_log_path}"
        )

try:
    default_level = settings.logging_level
except AttributeError:
    base_log.critical(
        f"'logging_level' missing in settings using {default_level}"
        )

try:
    default_file_level = settings.logging_file_level
except AttributeError:
    base_log.critical(
        f"'logging_log_level' missing in settings using {default_file_level}"
        )

try:
    default_auto_create = settings.logging_auto_create_dir
except AttributeError:
    base_log.critical(
        f"'logging_auto_create_dir' missing in settings using "
        f"{default_auto_create}"
        )

try:
    default_log_to_file = settings.logging_log_to_file
except AttributeError:
    base_log.critical(
        f"'logging_log_to_file' missing in settings using "
        f"{default_log_to_file}"
        )

try:
    default_log_ext = settings.logging_ext
except AttributeError:
    base_log.critical(
        f"'logging_ext' missing in settings using "
        f"{default_log_ext}"
        )

try:
    default_color = settings.color
except AttributeError:
    base_log.critical(
        f"'color' missing in settings using "
        f"{default_color}"
        )

if default_color:
    coloredlogs.install(logger=base_log)
log_path = os.path.normpath(default_log_path)

debug_levels = r"NOTSET|DEBUG|INFO|WARNING|ERROR|CRITICAL"


def set_log_path(
    path: str = log_path,
    auto_create: bool = default_auto_create
        ) -> str:
    """Set log path
    Set globally at load with config, can be called to modify path per module
    :param path: Direct or relative path for logfiles
    :param auto_create: Option to auto-create log directories
    :return: Log path
    """
    path = os.path.normpath(path)
    if not os.path.exists(path):
        if auto_create:
            create_path = "yes"
        else:
            create_path = py_option.inputYesNo(
                f"{path} does not exist\nWould "
                f"you like to create it?",
                limit=3,
                default="no",
                )
        if create_path == "yes":
            try:
                os.makedirs(path)
            except OSError as error:
                base_log.error(error)
                sys.exit(error)
        else:
            base_log.error("Log path not created")
            sys.exit("Log path not created")

    return path


def fix_mod_path(caller_name: str) -> str:
    """Get file name out of path
    :param caller_name: Path to check
    :return: Checked path
    """
    if ".py" in caller_name:
        caller_name = os.path.basename(caller_name)
        caller_name = caller_name.replace(".py", "")
    return caller_name


def verify_level(level: [str, int]) -> bool:
    """Verifies debug level
    :param level: Level to check
    """
    level_num = logging.getLevelName(level)
    invalid_level = "Level" in str(level_num)

    if invalid_level:
        exit_string = (f"ERROR - Invalid debug level\n"
                       f"Acceptable levels are:\nNOTSET, CRITICAL, "
                       f"DEBUG, INFO, WARNING, ERROR, CRITICAL\n"
                       f"or 0, 10, 20, 30, 40, 50\n"
                       f"You entered {level}")
        base_log.warning(exit_string)
        return False
    return True


def clear_logs(force: bool = False):
    """Delete log files
    :param force: No prompt
    :return:
    """
    file_list = []
    for files in os.listdir(log_path):
        if (os.path.isfile(os.path.join(log_path, files))
                and files[-len(default_log_ext):] == default_log_ext):
            file_list.append(os.path.join(log_path, files))
    if not file_list:
        base_logger.warning("No files to delete")
        return
    if not force:
        del_files = py_option.inputYesNo(
            f"There are {len(file_list)} log files in {log_path}\n"
            f"Do you want to delete all log files?",
            default="no",
            )
    else:
        del_files = "yes"

    if del_files == "yes":
        total_files = len(file_list)
        for del_file in file_list:
            try:
                os.remove(del_file)
            except IOError as err:
                base_logger.error(f"Unable to delete {del_file} - {err}")
                continue
            else:
                total_files -= 1
                base_logger.info(f"Deleted {del_file}")
        base_logger.info(
            f"Deleted {len(file_list) - total_files} of {len(file_list)} "
            f"file(s)"
            )
        dif_path = os.path.join(log_path, "diff")
        if os.path.isdir(dif_path):
            try:
                shutil.rmtree(dif_path)
            except IOError as err:
                base_logger.error(f"Unable to delete {dif_path} - {err}")
    else:
        base_logger.warning("Delete cancelled")


def get_parent_logger() -> [None, logging.Logger]:
    """Return logger from calling module
    :return:
    """
    stk = inspect.stack(0)
    ln = sys.argv[0]
    for fl in stk:
        if fl.filename == ln:
            for fs in fl.frame.f_locals:
                if type(fl.frame.f_locals.get(fs)) is logging.Logger:
                    return fl.frame.f_locals.get(fs)
    return None


class Timer:
    """Custom timer class
    :param level: Logging level to show timer at
    :type level: str
    """

    def __init__(self, level: str = default_level):
        self.start_time = 0
        self.end_time = 0
        self.logger = None
        self.stack = inspect.stack()
        self.frame = self.stack[1]
        self.caller = fix_mod_path(self.frame.filename)
        self.function = self.frame.function
        self.context = self.frame.code_context[0].strip().find("=")
        self.vid = self.frame.code_context[0].strip()[:self.context - 1]
        self.mod = inspect.getmodule(self.frame[0])
        try:
            self.logger = self.mod.__getattribute__("base_logger")
        except AttributeError:
            self.logger = base_logger
        self.logger.propagate = False
        if verify_level(level):
            self.level = level
        else:
            self.level = default_level
        try:
            self.logger.parent.handlers[0].setLevel(self.level)
        except IndexError:
            pass

    def start_timer(self, note: str = "", show_process: bool = False):
        """Start timer
        :param note: Note for logger
        :param show_process: Show process name in default message
        :return:
        """
        setattr(Timer, "svid", self.vid)
        local_func = inspect.getframeinfo(inspect.currentframe()).function
        fcaller = f"{self.caller}.{self.function}.{local_func}.{self.vid}"
        setattr(Timer, "scaller", fcaller)
        if not note:
            if show_process:
                logger_note = f"Timer started - {self.vid}"
            else:
                logger_note = "Timer started"
        else:
            logger_note = note.replace("%p%", self.vid)

        self.start_time = time.perf_counter()
        self.logger.log(logging.getLevelName(self.level), logger_note)
        setattr(Timer, "svid", "")
        setattr(Timer, "scaller", "")

    def stop_timer(self, note: str = "", show_process: bool = False):
        """Stop timer
        :param note: Note for logger
        :param show_process: Show process name in default message
        :return:
        """
        setattr(Timer, "svid", self.vid)
        local_func = inspect.getframeinfo(inspect.currentframe()).function
        fcaller = f"{self.caller}.{self.function}.{local_func}.{self.vid}"
        setattr(Timer, "scaller", fcaller)
        if not self.start_time:
            self.logger.log(
                logging.getLevelName(self.level),
                "Timer was not started"
                )
            setattr(Timer, "svid", "")
            setattr(Timer, "scaller", "")
            return

        self.end_time = time.perf_counter()
        total_time = self.end_time - self.start_time

        if not note:
            if show_process:
                logger_note = (f"Timer took {total_time:.3f} seconds - "
                               f"{self.vid}")
            else:
                logger_note = f"Timer took {total_time:.3f} seconds"
        else:
            logger_note = note.replace("%t%", "{:.3f}".format(total_time))

        self.logger.log(logging.getLevelName(self.level), logger_note)
        setattr(Timer, "svid", "")
        setattr(Timer, "scaller", "")
        self.start_time = 0


class Colors:
    """Wrapper for colorama"""

    class Fore:
        """Gets foreground code"""

        def __getattribute__(self, item):
            return getattr(colorama.Fore, item.upper())

    class Back:
        """Gets background code"""

        def __getattribute__(self, item):
            return getattr(colorama.Back, item.upper())

    class Style:
        """Gets style code"""

        def __getattribute__(self, item):
            return getattr(colorama.Style, item.upper())

    class Cursor:
        """Gets cursor code"""

        def __getattribute__(self, item):
            return getattr(colorama.Cursor, item.upper())


def text_color(text: str, style: str, attrib: str) -> str:
    """Get default colors and sets for level
    :param text: Text to be default color
    :param style: Style to reset
    :param attrib: Attribute to reset
    :return: Color
    :rtype: str
    """
    reset = ""
    if attrib.lower() == "fore":
        reset = Fore.RESET
    elif attrib.lower() == "back":
        reset = Back.RESET
    elif attrib.lower() == "style":
        reset = Style.RESET_ALL

    return (getattr(getattr(colorama, attrib.title()), style.upper()) + text +
            reset)


class CallerFilter(logging.Filter):
    """Class to add called variable to logger"""

    def __init__(self) -> None:
        super().__init__()
        self.name = "CallerFilter"

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Add spacers to record
        :param record: Record to check
        :type record: logging.LogRecord
        :return:
        :rtype: bool
        """

        spacers = (spacer_color +
                   spacer) * (58 - len(Timer().__getattribute__("scaller")))
        record.caller = f"{Timer().__getattribute__('scaller')} " f"{spacers}"
        record.varname = Timer().__getattribute__("svid")
        record.filefuncName = Timer().__getattribute__("scaller")
        return True


def get_logger(
    caller_name: str = __name__,
    level: [str, int] = default_level,
    log_to_file: bool = default_log_to_file,
    log_to_path: str = log_path,
    auto_create_path: bool = default_auto_create,
    log_file_level: [str, int] = default_file_level,
    color: bool = default_color
        ) -> logging.Logger:
    """Configures a logger
    :param caller_name: Name of module or custom name
    :param level: Debug level
    :param log_to_file: Logs to file in path set by set_log_path
    :param log_to_path: Can override default path per module
    :param auto_create_path: Auto create path for overridden path
    :param log_file_level: Level for file if different from base level
    :param color: Use coloredlogs
    :return: Logger
    :rtype: logging.Logger
    """
    if type(level) is not int:
        level = level.upper()
    if type(log_file_level) is not int:
        log_file_level = log_file_level.upper()
    if not verify_level(level):
        base_log.warning(f"Using {default_level}")
        level = default_level
    if not verify_level(log_file_level) and log_to_file:
        base_log.warning(f"Using {default_level}")
        log_file_level = default_level

    caller_name = fix_mod_path(caller_name)

    current_time = datetime.now()
    log_time = current_time.strftime("%m%d%y-%H%M")

    log_file_name = f"{caller_name}-{log_time}.{default_log_ext}"
    if log_path != log_to_path:
        log_to_path = set_log_path(log_to_path, auto_create=auto_create_path)
    log_full_path = os.path.join(log_to_path, log_file_name)

    log_formatter = logging.Formatter(
        fmt=file_log_format,
        datefmt="%Y-%m-%d %H:%M:%S"
        )

    logger = logging.getLogger(caller_name)
    logger.setLevel(level)
    logger.addFilter(NameFilter())

    if color:
        coloredlogs.install(logger=logger, level=level, fmt=console_log_format)
        try:
            logger.handlers[0].setLevel(level)
        except IndexError:
            pass

    if log_to_file:
        logger.info(f"Logging to {log_full_path}")
        log_file = logging.FileHandler(log_full_path)
        log_file.setLevel(log_file_level)
        log_file.setFormatter(log_formatter)
        logger.addHandler(log_file)

    return logger


if default_color:
    colorama.init(autoreset=True)
log_path = set_log_path()
if not verify_level(default_level):
    default_level = "DEBUG"
logging.basicConfig(level=default_level)
base_logger = logging.getLogger(__file__)

name_filter_added = False
for name_filter in base_logger.filters:
    if "NameFilter" in getattr(name_filter, "name", ""):
        name_filter_added = True

if not name_filter_added:
    base_logger.addFilter(NameFilter())
    if default_color:
        coloredlogs.install(
            logger=base_logger,
            fmt=caller_log_format,
            field_styles=caller_color_format,
            )

filter_added = False
for format_filters in base_logger.filters:
    if "CallerFilter" in str(format_filters.__getattribute__("name")):
        filter_added = True

if not filter_added:
    base_logger.addFilter(CallerFilter())
    if default_color:
        coloredlogs.install(
            logger=base_logger,
            fmt=caller_log_format,
            field_styles=caller_color_format,
            )

# Specific loggers
specific_loggers = {}
try:
    specific_loggers = dict(settings.specific_loggers)
except AttributeError:
    pass

if specific_loggers:
    for module, new_level in specific_loggers.items():
        valid_level = verify_level(new_level)
        if valid_level:
            try:
                logging.getLogger(module).setLevel(
                    logging.getLevelName(new_level)
                    )
            except AttributeError:
                base_logger.warning(
                    f"Cannot set logging on module '{module}' "
                    f"to '{logging.getLevelName(new_level)}'"
                    )
