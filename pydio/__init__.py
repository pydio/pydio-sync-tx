#! /usr/bin/env python
from zope.interface import Interface, Attribute

from twisted.application.service import IService


class IJob(Interface):
    """A pre-configured task that can be called repeatedly.
    IJobs are scheduled for execution by pydio.sched.Scheduler.
    """

    def do_job():
        """Perform one iteration of the job at hand"""


class ILooper(Interface):
    """Provides fine-grained control over periodic, deferred actions."""

    def start_loop(fn):
        """Enter the loop, calling `fn` at each iteration"""

    def stop_loop():
        """Exit the loop"""


class ISynchronizable(Interface):
    """Represents one side of a synchronization equation"""

    # idx = Attribute("Synchronization sequence index")

    def get_changes():
        """Get changes since last call"""

    def assert_ready():
        """Assert that ISynchronizable is available and consistent, i.e. it is
        ready to merge.
        """


class IMerger(Interface):
    """Implements merge logic for two or more ISynchronizables"""

    def sync():
        """Synchronize"""


class IWatcher(IService):
    """Monitors a directory for changes and notifies an EventHandler"""

    def register_handler(path, handler, recursive=True):
        """Register an IEventHandler to the watcher and receive notifications
        for events pertaining to the specified path.
        """


class IEventHandler(IService):
    """Receive events from an IWatcher"""

    def dispatch(ev):
        """Dispatches events to the appropriate methods"""

    def on_any_event(ev):
        """Catch-all callback"""


class IDiffHandler(IEventHandler):
    """Handle events pertaining to basic resource modification"""

    def on_created(ev):
        """Called when an inode is created"""

    def on_deleted(ev):
        """Called when an inode is deleted"""

    def on_modified(ev):
        """Called when an existing inode is modified"""

    def on_moved(ev):
        """Called when an existing inode is moved"""


class ISelectiveEventHandler(IEventHandler):
    include = Attribute("whitelist of UNIX glob patterns")
    exclude = Attribute("blacklist of UNIX glob patterns")

    def match_any(globlist, path):
        """Implements the matching logic using `include` and `exclude`"""


class IStateManager(Interface):
    """IStateManager receives changes to inodes and updates the state of an
    ISynchronizable, usually triggering the creation of a diff as a side-effect.
    """

    def create(inode, directory=False):
        """create an inode"""

    def delete(inode, directory=False):
        """delete an inode"""

    @_log_state_change("modify")
    def modify(inode, directory=False):
        """modify an inode"""

    @_log_state_change("move")
    def move(inode, directory=False):
        """move an inode"""
