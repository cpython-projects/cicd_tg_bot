import os
import pytest


@pytest.fixture(autouse=True)
def prepare_text_file(tmp_path):
    target_file = os.path.join(tmp_path, 'test.txt')
    with open(target_file, 'w', encoding='utf-8') as file:
        lines = [
            'Інженерія програмного забезпечення - БАКАЛАВР;https://pst.knu.ua/\n',
            'Інженерія програмного забезпечення - МАГІСТР;https://pst.knu.ua/\n',
            'Інженерія програмного забезпечення - ДОКТОР ФІЛОСОФІЇ;https://pst.knu.ua/',
        ]
        file.writelines(lines)
    return target_file
