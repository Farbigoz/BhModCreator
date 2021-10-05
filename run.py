import os
import sys
import traceback
import threading
import multiprocessing

from ui.utils.systemdialog import Error


def _bootstrap(self, parent_sentinel=None):
    import itertools
    from multiprocessing.process import _ParentProcess
    from multiprocessing import util, context
    global _current_process, _parent_process, _process_counter, _children

    try:
        if self._start_method is not None:
            context._force_start_method(self._start_method)
        _process_counter = itertools.count(1)
        _children = set()
        util._close_stdin()
        old_process = multiprocessing.current_process()
        _current_process = self
        _parent_process = _ParentProcess(
            self._parent_name, self._parent_pid, parent_sentinel)
        if threading._HAVE_THREAD_NATIVE_ID:
            threading.main_thread()._set_native_id()
        try:
            util._finalizer_registry.clear()
            util._run_after_forkers()
        finally:
            # delay finalization of the old process object until after
            # _run_after_forkers() is executed
            del old_process
        util.info('child process calling self.run()')
        try:
            self.run()
            exitcode = 0
        finally:
            util._exit_function()
    except SystemExit as e:
        if not e.args:
            exitcode = 1
        elif isinstance(e.args[0], int):
            exitcode = e.args[0]
        else:
            sys.stderr.write(str(e.args[0]) + '\n')
            exitcode = 1
    except:
        exitcode = 1
        sys.excepthook(*sys.exc_info())
    finally:
        threading._shutdown()
        util.info('process exiting with exitcode %d' % exitcode)
        util._flush_std_streams()

    return exitcode


multiprocessing.Process._bootstrap = _bootstrap


def handle_exception(exc_type, exc_value, exc_traceback):
    try:
        import pyi_splash
        pyi_splash.close()
    except:
        pass

    errorText = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))

    from main import ModCreator, PROGRAM_NAME, TerminateApp
    if ModCreator.app is not None:
        ModCreator.app.showError("Fatal Error:",
                                 errorText,
                                 terminate=True)
    else:
        Error(PROGRAM_NAME, errorText)
        TerminateApp()
        #sys.__excepthook__(exc_type, exc_value, exc_traceback)


sys.excepthook = handle_exception
threading.excepthook = lambda hook: handle_exception(hook.exc_type, hook.exc_value, hook.exc_traceback)


if __name__ == "__main__":
    from main import RunApp
    RunApp()
