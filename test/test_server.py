import unittest
import snap7
import ctypes


class TestServer(unittest.TestCase):
    def setUp(self):
        self.server = snap7.server.Server()
        self.server.start()

    def tearDown(self):
        self.server.stop()
        self.server.destroy()

    def test_register_area(self):
        db1_type = ctypes.c_char * 1024
        self.server.register_area(snap7.types.srvAreaDB, 3, db1_type())

    def test_error(self):
        self.server.error_text()

    @unittest.skip('not yet implemented')
    def test_callback(self):
        def event_call_back(event):
            pass
        self.server.set_events_callback(event_call_back)

    def test_error(self):
        for error in snap7.error.server_errors:
            snap7.common.error_text(error, client=False)

    def test_event(self):
        event = snap7.server.SrvEvent()
        snap7.server.event_text(event)

    def test_get_status(self):
        server, cpu, num_clients = self.server.get_status()

    def test_clear_events(self):
        self.server.clear_events()
        self.assertFalse(self.server.clear_events())

    def test_get_mask(self):
        self.server.get_mask(snap7.types.mkEvent)
        self.server.get_mask(snap7.types.mkLog)
        # invalid kind
        self.assertRaises(Exception, self.server.get_mask, 3)

    def test_get_param(self):
        # check the defaults
        self.assertEqual(self.server.get_param(snap7.types.LocalPort), 102)
        self.assertEqual(self.server.get_param(snap7.types.WorkInterval), 100)
        self.assertEqual(self.server.get_param(snap7.types.MaxClients), 1024)

        # invalid param for server
        self.assertRaises(Exception, self.server.get_param,
                          snap7.types.RemotePort)

    def test_lock_area(self):
        area_code = snap7.types.srvAreaDB
        index = 1
        db1_type = ctypes.c_char * 1024
        # we need to register first
        self.server.register_area(area_code, index, db1_type())
        self.server.lock_area(code=area_code, index=index)

    def test_pick_event(self):
        event = self.server.pick_event()
        self.assertEqual(type(event), snap7.server.SrvEvent)
        event = self.server.pick_event()
        self.assertFalse(event)

    def test_set_cpu_status(self):
        self.server.set_cpu_status(0)
        self.server.set_cpu_status(4)
        self.server.set_cpu_status(8)
        self.assertRaises(AssertionError, self.server.set_cpu_status, -1)

    def test_set_mask(self):
        self.server.set_mask(kind=snap7.types.mkEvent, mask=10)

    def test_set_param(self):
        param = snap7.types.MaxClients
        # TODO: we can't set params for the server?
        self.assertRaises(Exception, self.server.set_param, param, 2)

    def test_start_to(self):
        self.server.start_to('0.0.0.0')
        self.assertRaises(AssertionError, self.server.start_to, 'bogus')

    def test_unlock_area(self):
        area_code = snap7.types.srvAreaDB
        index = 1
        db1_type = ctypes.c_char * 1024

        # we need to register first
        self.assertRaises(Exception, self.server.lock_area, area_code, index)

        self.server.register_area(area_code, index, db1_type())
        self.server.lock_area(area_code, index)
        self.server.unlock_area(area_code, index)

    def test_unregister_area(self):
        area_code = snap7.types.srvAreaDB
        index = 1
        db1_type = ctypes.c_char * 1024
        self.server.register_area(area_code, index, db1_type())
        self.server.unregister_area(area_code, index)



if __name__ == '__main__':
    unittest.main()
