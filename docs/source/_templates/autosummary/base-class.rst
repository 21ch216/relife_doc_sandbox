{{ fullname | escape | underline}}

{% set exclude_methods = ["__init__", "__new__"] %}
{% set exclude_members = ", ".join(exclude_methods)  %}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
    :members:
    :inherited-members:
    :exclude-members: {{ exclude_members }}

    ==================
    {{ _('Methods') }}
    ==================

    .. autosummary::
        :nosignatures:

    {% for item in methods %}
        {% if item not in exclude_methods and not item.startswith('_') %}
            ~{{ name }}.{{ item }}
        {% endif %}
    {%- endfor %}

    ==================
    {{ _('Attributes') }}
    ==================

    .. autosummary::
        :nosignatures:

    {% for item in attributes %}
        {% if not item.startswith('_') %}
            ~{{ name }}.{{ item }}
        {% endif %}
    {%- endfor %}
