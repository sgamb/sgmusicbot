from shelf import Record


def get_track_file_ids(recordID: int) -> list[int]:
    record = Record.by_id(recordID)
    for track in record.tracks:
        yield track.file_id
