import dns.resolver


def get_mx_domains(hostname) -> [(int, str)]:
    """return list of (priority, domain name).
    domain name ends with a "." at the end.
    """
    try:
        answers = dns.resolver.query(hostname, "MX")
    except dns.resolver.NoAnswer:
        return []

    ret = []

    for a in answers:
        record = a.to_text()  # for ex '20 alt2.aspmx.l.google.com.'
        parts = record.split(" ")

        ret.append((int(parts[0]), parts[1]))

    return ret


_include_spf = "include:"


def get_spf_domain(hostname) -> [str]:
    """return all domains listed in *include:*"""
    try:
        answers = dns.resolver.query(hostname, "TXT")
    except dns.resolver.NoAnswer:
        return []

    ret = []

    for a in answers:  # type: dns.rdtypes.ANY.TXT.TXT
        for record in a.strings:
            record = record.decode()  # record is bytes

            if record.startswith("v=spf1"):
                parts = record.split(" ")
                for part in parts:
                    if part.startswith(_include_spf):
                        ret.append(part[part.find(_include_spf) + len(_include_spf) :])

    return ret


def get_txt_record(hostname) -> [str]:
    try:
        answers = dns.resolver.query(hostname, "TXT")
    except dns.resolver.NoAnswer:
        return []

    ret = []

    for a in answers:  # type: dns.rdtypes.ANY.TXT.TXT
        for record in a.strings:
            record = record.decode()  # record is bytes

            ret.append(a)

    return ret


def get_dkim_record(hostname) -> str:
    """query the dkim._domainkey.{hostname} record and returns its value"""
    try:
        answers = dns.resolver.query(f"dkim._domainkey.{hostname}", "TXT")
    except dns.resolver.NoAnswer:
        return ""

    ret = []
    for a in answers:  # type: dns.rdtypes.ANY.TXT.TXT
        for record in a.strings:
            record = record.decode()  # record is bytes

            ret.append(record)

    return "".join(ret)
