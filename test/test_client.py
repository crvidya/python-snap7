import unittest
import snap7
import ctypes
import logging

logging.basicConfig()
l = logging.getLogger()
l.setLevel(logging.INFO)

#ip = '192.168.200.24'
ip = '127.0.0.1'
db_number = 1
rack = 1
slot = 1


class TestClient(unittest.TestCase):

    def setUp(self):
        self.client = snap7.client.Client()
        self.client.connect(ip, rack, slot)

    def tearDown(self):
        self.client.disconnect()
        self.client.destroy()

    def test_db_read(self):
        size = 40
        start = 0
        db = 1
        type_ = snap7.types.wordlen_to_ctypes[snap7.types.S7WLByte]
        data = (type_ * size)()
        data = bytearray(data)
        self.client.db_write(db_number=db, start=start, size=size, data=data)
        result = self.client.db_read(db_number=db, start=start, size=size,
                                     type_=type_)
        self.assertEqual(bytearray(data), result)

    def test_db_write(self):
        size = 40
        data = (snap7.types.wordlen_to_ctypes[snap7.types.S7WLByte] * size)()
        data = bytearray(data)
        self.client.db_write(db_number=1, start=0, size=size, data=data)

    def test_db_get(self):
        self.client.db_get(db_number=db_number)

    @unittest.skip('authorization required?')
    def test_db_upload(self):
        data = snap7.client.buffer_type()
        self.client.db_upload(block_type=snap7.types.block_types['DB'],
                              block_num=db_number, data=data)

    def test_read_area(self):
        area = snap7.types.S7AreaDB
        dbnumber = 1
        amount = 10
        start = 1
        wordlen = snap7.types.S7WLByte
        self.client.read_area(area, dbnumber, start, amount, wordlen)

    def test_write_area(self):
        area = snap7.types.S7AreaDB
        dbnumber = 1
        amount = 10
        start = 1
        wordlen = snap7.types.S7WLByte
        data = (ctypes.c_int16 * amount)()
        self.client.write_area(area, dbnumber, start, amount, wordlen, data)

    def test_list_blocks(self):
        blockList = self.client.list_blocks()
        print blockList

    def test_list_blocks_of_type(self):
        self.client.list_blocks_of_type(snap7.types.block_types['DB'], 10)

    def test_set_session_password(self):
        password = 'abcdefgh'
        self.client.set_session_password(password)

    def test_clear_session_password(self):
        self.client.clear_session_password()


if __name__ == '__main__':
    unittest.main()
