# Copyright 2018 Autodesk, Inc.  All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license agreement
# provided at the time of installation or download, or which otherwise accompanies
# this software in either electronic or hard copy form.
#
from .handlers.ticket_enable_sync_handler import TicketEnableSyncingHandler
from .handlers.ticket_issue_handler import TicketIssueHandler
from .handlers.ticket_reply_comment_handler import TicketReplyCommentHandler
from .syncer import Syncer


class TicketIssueSyncer(Syncer):
    """
    Sync Shotgun Tasks as Jira Issues.
    """

    def __init__(self, issue_type="Task", **kwargs):
        """
        Instatiate a new Task/Issue syncer for the given bridge.

        :param str issue_type: Jira Issue type to use when creating new Issues.
        """
        self._issue_type = issue_type
        super(TicketIssueSyncer, self).__init__(**kwargs)
        self._ticket_issue_handler = TicketIssueHandler(self, self._issue_type)
        self._reply_comment_handler = TicketReplyCommentHandler(self)
        # A handler combining the Task <-> Issue handler and the Note <-> Comment
        # handler. Task syncing to Jira starts if the Task "Sync in Jira" checkbox
        # is turned on. Notes linked to a Task being actively synced are automatically
        # synced without having to manually select them. A full sync is performed
        # when the Task checkbox is turned on.
        self._enable_syncing_handler = TicketEnableSyncingHandler(
            self,
            [self._ticket_issue_handler, self._reply_comment_handler]
        )

    @property
    def handlers(self):
        """
        Return a list of :class:`~handlers.SyncHandler` instances.
        """
        return [
            self._enable_syncing_handler,
            self._ticket_issue_handler,
            self._reply_comment_handler
        ]
