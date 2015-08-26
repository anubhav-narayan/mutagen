# -*- coding: utf-8 -*-
# Copyright (C) 2005  Michael Urman
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of version 2 of the GNU General Public License as
# published by the Free Software Foundation.


class PaddingInfo(object):
    """Abstract padding information object.

    This will be passed to the callback function that can be used
    for saving tags.

    ::

        def my_callback(info: PaddingInfo):
            return info.get_default_padding()

    The callback should return the amount of padding to use (>= 0) based on
    the content size and the padding of the file after saving. The actual used
    amount of padding might vary depending on the file format (due to
    alignment etc.)

    The default implementation can be accessed using the
    :meth:`get_default_padding` method in the callback.
    """

    padding = 0
    """The amount of padding left after saving in bytes (can be negative if
    more data needs to be added as padding is available)
    """

    size = -1
    """The size of the file in bytes after saving minus padding or -1 if
    unknown.
    """

    def __init__(self, padding, filesize):
        self.padding = padding
        if filesize >= 0:
            self.size = filesize - padding
            if self.size < 0:
                raise ValueError("Invalid padding")
        elif filesize == -1:
            self.size = -1
        else:
            raise ValueError("Invalid filesize")

    def get_default_padding(self):
        """The default implementation which tries to select a reasonable
        amount of padding and which might change in future versions.

        :return: Amount of padding after saving
        :rtype: int
        """

        # larger files are slower to resize, so try to leave more padding there
        high = 1024 * 5
        low = 1024
        if self.size != -1:
            high += self.size // 40  # 2.5%
            low += self.size // 200  # 0.5%

        if self.padding >= 0:
            # enough padding left
            if self.padding > high:
                # padding too large, reduce
                return low
            # just use existing padding as is
            return self.padding
        else:
            # not enough padding, add some
            return low

    def _get_padding(self, user_func):
        if user_func is None:
            return self.get_default_padding()
        else:
            return user_func(self)

    def __repr__(self):
        return "<%s size=%d padding=%d>" % (
            type(self).__name__, self.size, self.padding)


class Metadata(object):
    """An abstract dict-like object.

    Metadata is the base class for many of the tag objects in Mutagen.
    """

    __module__ = "mutagen"

    def __init__(self, *args, **kwargs):
        if args or kwargs:
            self.load(*args, **kwargs)

    def load(self, *args, **kwargs):
        raise NotImplementedError

    def save(self, filename=None):
        """Save changes to a file."""

        raise NotImplementedError

    def delete(self, filename=None):
        """Remove tags from a file."""

        raise NotImplementedError
