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


Likelihoods
~~~~~~~~~~~

.. autosummary::
    :toctree: likelihood
    :template: base-class.rst
    :caption: Likelihoods

    LikelihoodFromLifetimes

Base class
~~~~~~~~~~~

What we call `base class` are objects (in Python class are objects) used at the core of ReLife subsystems.
For beginners, it is not necessary to know them. If you start to inspect ReLife code, you will encounter them regularly
in inheritance hierarchy. In fact, most objects created for fiability theory inherits from one of those objects. One can
think of them as `engines` that empower objects with special functionalities to make ReLife model creation easier.


.. rubric:: Models

.. autosummary::
    :toctree: base_class
    :template: base-class.rst
    :caption: Base class

    LifetimeModel

.. rubric:: Parametric models

.. autosummary::
    :toctree: base_class
    :template: base-class.rst


    Parameters
    ParametricModel
    ParametricLifetimeModel
