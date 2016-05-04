"""
Output only rows for addresses in Chicago, IL.

Excludes PO Boxes.
"""
# !/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import pandas as pd


def drop_PO_box(df, check='BOX '):
    """Filter PO Box addresses."""
    return df[~df['ADDRESS'].str.contains(check)]


def drop_outside_IL(df, check='IL'):
    """Filter addresses outside IL."""
    return df[df['STATE'].str.contains(check)]


def drop_outside_Chicago(df, check='CHICAGO'):
    """Filter addresses outside Chicago."""
    return df[df['CITY'] == check]

# load in business data
df = pd.read_csv(sys.stdin, low_memory=False)
# Filter addresses for only street address in Chicago, IL
chicago_df = drop_PO_box(df)
chicago_df = drop_outside_IL(chicago_df)
chicago_df = drop_outside_Chicago(chicago_df)

# SAVE OUTPUT
chicago_df.to_csv(sys.stdout, index=False)
