import logging

from dateutil.parser import parse as dt_parse


def valid_d3mindex(d3m_column):
    for entry in d3m_column:
        try:
            val = int(entry)
            if val < 0:
                logging.error(f"{val} is not a valid d3mindex value.")
                return False
        except ValueError:
            logging.error(f"{entry} is not a valid d3mindex value.")
            return False

    return True


def valid_boolean(boolean_column):
    unique_entries = set()
    for entry in boolean_column:
        if not is_castable_to_type(entry, int) and not isinstance(entry, str):
            logging.error(
                f"{entry} is not a string or an integer which is required of boolean types."
            )
            return False

        unique_entries.add(entry)

    if len(unique_entries) > 2:
        logging.error(
            f"The set of unqiue entries: {unique_entries} has more than two elements"
            f"which is too many to be interpreted as boolean."
        )
        return False
    return True


def valid_real(float_column):
    for entry in float_column:
        if not is_castable_to_type(entry, float):
            logging.error(f"The entry: {entry} could not be converted to a float.")
            return False
    return True


def valid_integer(int_column):
    for entry in int_column:
        if not is_castable_to_type(entry, int) or float(entry) != float(int(entry)):
            logging.error(f"The entry: {entry} could not be converted to an integer")
            return False
    return True


def valid_string(text_column):
    for entry in text_column:
        if not isinstance(entry, str):
            logging.error(f"The entry: {entry} is not a string.")
            return False
    return True


def valid_categorical(cat_column, authorized_labels=None):

    # "Invalid" means that the predicted categorical value doesn't appear in the
    # targets.csv file
    invalid_values_detected = False

    for entry in cat_column:
        if not is_castable_to_type(entry, int) and not isinstance(entry, str):
            logging.error(
                f"The entry: {entry} could not be converted to an integer or a string."
            )
            return False

        if authorized_labels and entry not in authorized_labels:
            invalid_values_detected = True

    if invalid_values_detected:
        logging.warning(
            f"Some categorical entries didn't match any entry in the targets file"
        )

    return True


def valid_datetime(datetime_column):
    for entry in datetime_column:

        if not isinstance(entry, str):
            logging.error(f"The entry: {entry} is not a string.")
            return False

        try:
            dt_parse(entry)
        except ValueError:
            logging.error(f"The entry: {entry} is not in a valid datetime format.")
            return False

    return True


def is_castable_to_type(value, vtype):
    try:
        vtype(value)
    except ValueError:
        return False
    return True
