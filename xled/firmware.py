def update_0(control, firmware):
    """
    Uploads first stage of the firmware

    :param firmware: file-like object that points to firmware file.
    :raises ApplicationError: on application error
    :rtype: :class:`~xled.response.ApplicationResponse`
    """
    return control._post("fw/0/update", data=firmware)


def update_(control, firmware):
    """
    Uploads second stage of the firmware

    :param firmware: file-like object that points to firmware file.
    :raises ApplicationError: on application error
    :rtype: :class:`~xled.response.ApplicationResponse`
    """
    return control._post("fw/1/update", data=firmware)


def update(control, stage0_sha1sum, stage1_sha1sum=None):
    """
    Performs firmware update from previously uploaded images

    :param str stage0_sha1sum: SHA1 digest of first stage
    :param str stage1_sha1sum: SHA1 digest of second stage
    :raises ApplicationError: on application error
    :rtype: :class:`~xled.response.ApplicationResponse`
    """
    if stage1_sha1sum is not None:
        json_payload = {
            "checksum": {
                "stage0_sha1sum": stage0_sha1sum,
                "stage1_sha1sum": stage1_sha1sum,
            }
        }
    else:
        json_payload = {
            "checksum": {
                "stage0_sha1sum": stage0_sha1sum,
            }
        }

    return control._post("fw/update", json=json_payload)


def version(control):
    """
    Gets firmware version

    :raises ApplicationError: on application error
    :rtype: :class:`~xled.response.ApplicationResponse`
    """
    return control._get("fw/version", u"version", u"code")
