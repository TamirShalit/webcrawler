import tabulate

from webcrawler import analyzers, utils
from webcrawler.raw_material import FlightLandingUpdate

from conf import RAW_MATERIAL_DIR, SEARCHED_WORD


def main():
    landing_files_from_istanbul = analyzers.search_for_text_in_material_directory(FlightLandingUpdate,
                                                                                  RAW_MATERIAL_DIR,
                                                                                  SEARCHED_WORD)
    landing_updates_from_istanbul = utils.load_raw_material_from_files(FlightLandingUpdate,
                                                                       landing_files_from_istanbul)

    recent_landing_updates_from_istanbul = utils.get_most_recent_landing_updates(
        landing_updates_from_istanbul)
    _pretty_print_searched_updates(recent_landing_updates_from_istanbul)


def _pretty_print_searched_updates(recent_landing_updates_from_istanbul):
    table = []
    for landing_update in recent_landing_updates_from_istanbul:
        table.append((landing_update.flight_number, landing_update.planned_time,
                      landing_update.updated_time, landing_update.terminal,
                      landing_update.company))
    print '---------------Landings from Istanbul---------------\n\n'
    tabulate_tabulate = tabulate.tabulate(table, headers=(
        'Flight Number', 'Planned Landing', 'Updated Landing', 'Terminal', 'Company'))
    print tabulate_tabulate


if __name__ == '__main__':
    main()
