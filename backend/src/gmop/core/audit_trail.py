import logging


def audit_log_info(username, event):
    logging.getLogger("audit_trail").info(f"{username} : {event}")
