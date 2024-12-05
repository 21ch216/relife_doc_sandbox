API
=============

.. currentmodule:: relife2

Lifetime models
~~~~~~~~~~~~~~~


.. rubric:: Distribution models

.. autosummary::
    :toctree: distribution
    :template: parametric-lifetime-model-class.rst
    :caption: Lifetime distribution models

    Exponential
    Weibull
    Gompertz
    Gamma
    LogLogistic


.. rubric:: Regression models

.. autosummary::
    :toctree: regression
    :template: parametric-lifetime-model-class.rst
    :caption: Lifetime regression models

    ProportionalHazard
    AFT

Non-parametric estimators
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: nonparametric
    :template: parametric-lifetime-model-class.rst
    :caption: Non parametric lifetime estimators

    ECDF
    KaplanMeier
    NelsonAalen
    Turnbull


Base models
~~~~~~~~~~~

.. rubric:: Parametric models

.. autosummary::
    :toctree: model
    :template: parametric-lifetime-model-class.rst
    :caption: Base models

    ParametricModel
    ParametricLifetimeModel
