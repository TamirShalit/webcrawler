import os

from newscollector.raw_material import JsonRawMaterial


def _get_lowered_list(iterable):
    lowered_list = []
    for element in iterable:
        if isinstance(element, basestring):
            lowered_list.append(element.lower())
        else:
            lowered_list.append(element)
    return lowered_list


def has_text(raw_material, text, case_sensitive=False):
    """Whether the material contains a certian text."""
    if not case_sensitive:
        text = text.lower()
    if hasattr(raw_material, 'to_text'):
        return _has_text_in_text_material(raw_material, text, case_sensitive)
    if isinstance(raw_material, JsonRawMaterial):
        return _has_text_in_json_material(text, raw_material, case_sensitive)
    raise NotImplementedError('No analyzer for this type of material.')


def _has_text_in_text_material(raw_material, text, case_sensitive):
    searched_text = raw_material.to_text()
    if not case_sensitive:
        searched_text = searched_text.lower()
    return text in searched_text


def _has_text_in_json_material(text, raw_material, case_sensitive):
    material_dict = raw_material.to_dict()
    searched_keys = material_dict.keys()
    searched_values = material_dict.values()
    if not case_sensitive:
        searched_keys = _get_lowered_list(searched_keys)
        searched_values = _get_lowered_list(searched_values)
    return text in searched_keys or text in searched_values


def search_for_text_in_material_files(material_type, file_paths, text, case_sensitive=False):
    """
    Search for text in files properly dumped from `RawMaterial` instances.

    :param material_type: The type of material the files represent.
    :type material_type: Subclass of `RawMaterial`
    :param file_paths: Paths of the files to search text in.
    :type file_paths: list[str]
    :param text: Text to search
    :type text: str
    :param case_sensitive: Whether to search the text with matched case.
    :type case_sensitive: bool
    :return: List of file paths which contain the searched text.
    :rtype: list[str]
    """
    files_with_text = []
    for file_path in file_paths:
        raw_material = material_type.load(file_path)
        if has_text(raw_material, text, case_sensitive):
            files_with_text.append(file_path)
    return files_with_text


def search_for_text_in_material_directory(material_type, directory_path, text,
                                          case_sensitive=False):
    """
    Search for text in directory.
    Read `search_for_text_in_material_files` for further documentation.
    """
    file_paths = [os.path.join(directory_path, file_name) for file_name in
                  os.listdir(directory_path)]
    return search_for_text_in_material_files(material_type, file_paths, text, case_sensitive)
