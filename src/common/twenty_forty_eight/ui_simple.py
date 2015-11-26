import logging


class Ui:
    @staticmethod
    def update_ui(state):
        divider = '------------------\n'
        string = str('\n%s' % divider)

        for i in [0, 1, 2, 3]:
            string += '|'

            for j in [0, 1, 2, 3]:
                cell = state[i][j]

                if cell:
                    char = '0%d' % cell.value if cell.value < 10 else str(cell.value)

                    string += ' %s ' % char
                else:
                    string += '    '

            string += '|\n%s' % divider

        logging.info(string)
