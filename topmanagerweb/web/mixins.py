# -*- coding: utf-8 -*-
# web/mixins.py

from django.shortcuts import redirect
from django.core.exceptions import ImproperlyConfigured


class FilterMixin(object):
    '''View mixin which provides filtering for listview.

    Attributes:
        filter_url_kwarg (str): Url slug to get the filter param, default `filter`.
        default_filter_param (str): Default filter param, default None.

    '''
    filter_url_kwarg = 'filter'
    default_filter_param = None

    def get_default_filter_param(self):
        '''Gets the default filter param.

        Returns:
            str: Default filter param.

        Raises:
            ImproperlyConfigured: If `default_filter_param` is None.

        '''
        if self.default_filter_param is None:
            msg = u'`FilterMixin` requires the `default_filter_param` attribute to be set.'

            raise ImproperlyConfigured(msg)

        return self.default_filter_param

    def filter_queryset(self, qs, filter_param):
        '''Filter the queryset `qs`, given the selected `filter_param`.

        Default implementation does no filtering at all.

        Args:
            qs (QuerySet): Queryset to filter.
            filter_param (str): Param to be filter.

        Returns:
            QuerySet: Filtered queryset.

        '''
        return qs

    def get_filter_param(self):
        '''Gets the filter param from kwargs.

        Returns:
            str: Filter param, default `default_filter_param`.

        '''
        return self.kwargs.get(self.filter_url_kwarg, self.get_default_filter_param())

    def get_queryset(self):
        '''Gets the filtered queryset by the filter param.

        Returns:
            QuerySet: Filtered queryset.

        '''
        return self.filter_queryset(super(FilterMixin, self).get_queryset(),
                                    self.get_filter_param())

    def get_context_data(self, *args, **kwargs):
        '''Adds the filter to the context data.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            dict: Context data.

        '''
        context = super(FilterMixin, self).get_context_data(*args, **kwargs)

        context.update({
            u'filter': self.get_filter_param(),
        })

        return context


class LoginRequiredMixin(object):
    '''View mixin which requires that the user is authenticated.

    '''
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        '''Override the `dispatch` method of the object.

        Checks if the user is logged. If False, redirect to the login page.

        Args:
            request (HttpRequest): Request object received.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpRequest: If the user is not logged.
            function: Otherwise.

        '''
        return super(LoginRequiredMixin, self).dispatch(self, request, *args, **kwargs)


class SortMixin(object):
    '''View mixin which provides sorting for ListView.

    Attributes:
        default_sort_param (str): Default filter param, default None.

    '''
    default_sort_params = None

    def sort_queryset(self, qs, sort_by, order):
        '''Order the queryset `qs`, given the `sort_by` and the `order`.

        Default implementation does no sorting at all.

        Args:
            qs (QuerySet): Queryset to sort.
            sort_by (str): Field to be sorted by.
            order (str): Order `ASC` or `DESC`.

        Returns:
            QuerySet: Filtered queryset.

        '''
        return qs

    def get_default_sort_params(self):
        '''Gets the default sort params.

        Returns:
            str: Default sort params.

        Raises:
            ImproperlyConfigured: If `default_sort_params` is None.

        '''
        if self.default_sort_params is None:
            msg = u'`SortMixin` requires the `default_sort_params` attribute to be set.'

            raise ImproperlyConfigured(msg)

        return self.default_sort_params

    def get_sort_params(self):
        '''Gets the sort params from kwargs.

        Returns:
            tuple: (Sort params, order)`, default `default_sort_params`.

        '''
        default_sort_by, default_order = self.get_default_sort_params()

        sort_by = self.request.GET.get(u'sort_by', default_sort_by)
        order = self.request.GET.get(u'order', default_order)

        return (sort_by, order)

    def get_queryset(self):
        '''Gets the sorted queryset by the sort params.

        Returns:
            QuerySet: Ordered queryset.

        '''
        return self.sort_queryset(super(SortMixin, self).get_queryset(),
                                  *self.get_sort_params())

    def get_context_data(self, *args, **kwargs):
        '''Adds the ordering info to the context data.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            dict: Context data.

        '''
        context = super(SortMixin, self).get_context_data(*args, **kwargs)
        sort_by, order = self.get_sort_params()

        context.update({
            u'sort_by': sort_by,
            u'order': order,
        })

        return context


class StaffRequiredMixin(object):
    '''View mixin which requires that the authenticated user is a staff member.

    (i.e. `is_staff` is True).

    Attributes:
        msg (str): Forbidden access message.
        not_logged_url (str): Url to redirect when the user is not a staff member.

    '''
    msg = 'You do not have the permission required to perform the requested operation.'
    not_logged_url = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        '''Override the `dispatch` method of the object.

        Checks if the user is a staff member. If False, redirect to the `not_logged_url`.

        Args:
            request (HttpRequest): Request object received.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpRequest: If the user is not logged.
            function: Otherwise.

        '''
        if not request.user.is_staff:
            messages.error(request, self.msg)

            return redirect(self.get_not_logged_url())

        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)

    def get_not_logged_url(self):
        '''Gets the url when the user is not a staff member.

        Returns:
            str: Url when the user is not a staff member.

        Raises:
            ImproperlyConfigured: If `not_logged_url` is None.

        '''
        if self.not_logged_url is None:
            msg = u'`StaffRequiredMixin` requires the `not_logged_url` attribute to be set.'

            raise ImproperlyConfigured(msg)

        return self.not_logged_url


class SuperUserRequiredMixin(object):
    '''View mixin which requires that the authenticated user is a super user.

    (i.e. `is_superuser` is True).

    Attributes:
        msg (str): Forbidden access message.
        not_logged_url (str): Url to redirect when the user is not a super user.

    '''
    msg = u'You do not have the permission required to perform the requested operation.'
    not_logged_url = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        '''Override the `dispatch` method of the object.

        Checks if the user is a super user. If False, redirect to the `not_logged_url`.

        Args:
            request (HttpRequest): Request object received.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpRequest: If the user is not logged.
            function: Otherwise.

        '''
        if not request.user.is_superuser:
            messages.error(request, self.msg)

            return redirect(self.get_not_logged_url())

        return super(SuperUserRequiredMixin, self).dispatch(request, *args, **kwargs)

    def get_not_logged_url(self):
        '''Gets the url when the user is not a super user.

        Returns:
            str: Url when the user is not a super user.

        Raises:
            ImproperlyConfigured: If `not_logged_url` is None.

        '''
        if self.not_logged_url is None:
            msg = u'`SuperUserRequiredMixin` requires the `not_logged_url` attribute to be set.'

            raise ImproperlyConfigured(msg)

        return self.not_logged_url
