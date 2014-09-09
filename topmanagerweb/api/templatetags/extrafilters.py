# -*- coding: utf-8 -*-
# api/views.py

from django import template


register = template.Library()


@register.filter(is_safe=True)
def visible0(total, current):
      '''Gets the visible range of zero pages for the paginator's current page.

      Args:
          total (int): Paginator's total pages number.
          current (int): Paginator's current page number.

      Returns:
          list of int: Pages visible range.

      '''
      return get_visible_range(total, current, adyacents=0)


@register.filter(is_safe=True)
def visible1(total, current):
      '''Gets the visible range of one page for the paginator's current page.

      Args:
          total (int): Paginator's total pages number.
          current (int): Paginator's current page number.

      Returns:
          list of int: Pages visible range.

      '''
      return get_visible_range(total, current, adyacents=1)


@register.filter(is_safe=True)
def visible2(total, current):
      '''Gets the visible range of two pages for the paginator's current page.

      Args:
          total (int): Paginator's total pages number.
          current (int): Paginator's current page number.

      Returns:
          list of int: Pages visible range.

      '''
      return get_visible_range(total, current, adyacents=2)


@register.filter(is_safe=True)
def visible3(total, current):
      '''Gets the visible range of three pages for the paginator's current page.

      Args:
          total (int): Paginator's total pages number.
          current (int): Paginator's current page number.

      Returns:
          list of int: Pages visible range.

      '''
      return get_visible_range(total, current, adyacents=3)


@register.filter(is_safe=True)
def visible4(total, current):
      '''Gets the visible range of four pages for the paginator's current page.

      Args:
          total (int): Paginator's total pages number.
          current (int): Paginator's current page number.

      Returns:
          list of int: Pages visible range.

      '''
      return get_visible_range(total, current, adyacents=4)


@register.filter(is_safe=True)
def visible5(total, current):
      '''Gets the visible range of five pages for the paginator's current page.

      Args:
          total (int): Paginator's total pages number.
          current (int): Paginator's current page number.

      Returns:
          list of int: Pages visible range.

      '''
      return get_visible_range(total, current, adyacents=5)


def get_visible_range(total, current, adyacents):
      '''Gets the visible range of adyacents pages for the paginator's current page.

      Args:
          total (int): Paginator's total pages number.
          current (int): Paginator's current page number.
          adyacents (int): Adyacents visible pages number.

      Returns:
          list of int: Pages visible range.

      '''
      first = (current - adyacents) if current > adyacents else 1
      end = (current + adyacents) if current <= total-adyacents else total

      return range(first, end+1)
