This page aims at providing succint explanations on refactoring
choices.

On Numpy dependance
===================

User knows numpy
----------------

We expect user to know ``numpy`` and to understanc basics of
`broadcasting <https://numpy.org/doc/stable/user/basics.broadcasting.html>`__.
As a consequence, most methods inputs are supposed to be ``np.array``
object and we **did not add control on user inputs nor user inputs
automatic conversion**

Numpy objects dim
-----------------

All numpy objects inputs never have more than 2 dimensions.

-  ``0d-array`` : one point of measure
-  ``1d-array`` : :math:`n` points of measure on 1 unit, shape
   :math:`(n,)`
-  ``2d-array`` : :math:`n` points of measure on :math:`m` units, shape
   :math:`(m,)`

Subsystems operations are written in numpy meaning *broadcastable*. So
we expect user to write correctly its inputs and to know in advance what
kind of shape is expecting.

Models framework
================

When a model is composed of several parametric parts, which can
themselves be other ``ParametricModel`` objects, it can be challenging
to create a new model without disrupting the overall logic of the ReLife
implementations. To assist with the implementation of new statistical
models, we have implemented *framework* objects called ``Parameters``
and ``ParametricComponent``. These objects provide helpful properties
and operations to simplify the creation of new parametric models.

The ``Parameters`` object is used to encode the parameters of a whole
model while preserving the composition structure of models. It can be
seen as a tree of parameter sets that follows the tree of model
composition. Additionally, it provides a set of helper properties and
operations that make it easier to define and work with the parameters of
a parametric model.

The ``ParametricComponent`` object, on the other hand, is used to
represent a single parametric part of a model. It is composed of a
``Parameters`` instance and provides a unified interface for adding new
components to existing ones, similar to function composition. It can be
seen as a tree of parametric functions.

By using these framework objects, it is possible to more easily create
new parametric models that are composed of multiple parts, without
having to worry about disrupting the overall logic of the ReLife
implementations.

``Parameters``
--------------

In previous versions of ReLife, model parameters were encapsulated in a
varying-sized list of floats, depending on the number of parameters. The
``Parameters`` object is a more powerful alternative to this simple
list, and it has been implemented to encapsulate the structure and
values of the parameters. This object is responsible for automatically
adapting the storage of parameters in a ``ParametricComponent`` and
ensuring that parameters follow the structure of model composition. We
have adapted the `composite
pattern <https://en.wikipedia.org/wiki/Composite_pattern>`__ to encode
parameters in a tree structure that follows the composition of the
model. Our ``Parameters`` objects can be seen as a tree of dictionaries.

Each node in the tree has:

-  A dictionary of parameter names and values
-  All parameter names and values stored in lists (including those from
   the current node and all leaf nodes)

This allows for multiple nodes to have the same parameter names.
Separating the dictionary of current node parameters and lists of all
parameters is mainly due to computation constraints. When operations
modify all parameters of a model, it avoids the need to read the entire
parameter tree each time.

Each node can answer several requests, including:

-  Getting/setting all parameter values from a node (updating the
   current node’s parameter values and those of its leaves)
-  Getting/setting all parameter names from a node (updating the current
   node’s parameter names and those of its leaves)
-  Getting/setting a parameter from its name at the node level (avoiding
   the ability to call other node parameters by name to prevent naming
   conflicts)
-  Modifying the entire set of parameter names and values, including
   their number (updating the current node’s dictionary of parameters)

I hope this revised text is clear and helpful. Let me know if you have
any further questions or concerns.

**improvements :** - replace composite by
`namedtuple <https://docs.python.org/fr/3/library/collections.html#collections.namedtuple>`__
and do not store all params and all names (not really used)

``ParametricComponent``
-----------------------

The ``ParametricComponent`` object also follows a tree-like structure,
as it stores other ``ParametricComponent`` objects in its ``leaves``
attribute. It benefits from the ``__getattr__`` and ``__setattr__``
Python magic methods, which create a sort of bridge with the parameters
data in order to call parameters by their names inside methods.

A ``ParametricComponent`` object has the following attributes:

-  ``params``: This is composed of a ``Composite`` object and contains
   the parameters for the current node.
-  ``leaves``: This is a list of other ``ParametricComponent`` objects.

The ``ParametricComponent`` object has the following methods:

-  ``compose_with``: This method adds a ``ParametricComponent`` object
   as a leaf that can be called from the current node.
-  ``new_params``: This method changes the local parameters structure at
   the node level.

``LifetimeModel`` baseclass : implementation control
----------------------------------------------------

``LifetimeModel`` provides a base interface consisting of survival
probability functions, and any subclass of ``LifetimeModel`` must
implement a minimum set of these functions. The ``LifetimeModel`` class
controls the existence of certain probability functions, such as ``sf``,
``hf``, etc., by looking at class attributes. Then, ``LifetimeModel``
provides base implementations for all common survival probability
functions.

One major change in the ``LifetimeModel`` class is that it no longer
relies on the ``ABC`` module. The specific set of concrete method
implementations needed in a ``LifetimeModel`` subclass will vary
depending on which methods have already been implemented. For example,
if a subclass implements ``hf`` and ``pdf``, it can compute ``sf`` using
a specific formula. But if a subclass implements ``sf`` and ``pdf``, it
will not need to implement ``hf``, because it can be computed using a
different formula. Using ``abstractmethod`` would not be appropriate in
this case, because it would require that the minimum set of mandatory
probability functions remains the same. Instead, we can use the old
abstract class style and raise a ``NotImplementedError`` when a
particular function is needed but has not been implemented. The specific
probability formula used will depend on which methods are present in the
``LifetimeModel`` derived class, which can be determined by looking at
class attributes (e.g., using an ``if … in self.__class__.__dict__``
condition).

Additionally, we can prevent the ``LifetimeModel`` class from being
instantiated by overriding the ``__new__`` method. This avoids clumsy
usage of this class and implementing a metaclass would have been
cumbersome.

**improvements** :

-  with ``__init_subclass__`` read methods signature recursively in
   order to to parse \*args names and to fill args_names and nb_args

Variadic model ``args`` : ``LifetimeModel`` is ``Generic``
----------------------------------------------------------

In previous versions of ReLife, the unpacking operator ``*`` was used to
create an infinite number of arguments that could be passed to a
function. This allowed the ``LifetimeModel`` interface to be responsive
to a variadic number of extra arguments in methods signatures when the
model was composed of other models. The following piece of code
illustrates this idea in the case of a regression model:

.. code:: python

   class LifetimeModel:
       ...
       def hf(self, time: NDArray[np.float64], *args: NDArray[np.float64]):...

   class ProportionalHazard(LifetimeModel):
       baseline : LifetimeModel
       ...
       def hf(self, time: NDArray[np.float64], covar : NDArray[np.float64], *args: NDArray[np.float64]):...
           return self.covar_effect.g(covar) * self.baseline.hf(time, *args)

In this example, ``ProportionalHazard`` objects are composed of any
other ``LifetimeModel`` instance and inherit the ``LifetimeModel``
interface in order to reuse the base implementation of probability
functions if needed. However, ``ProportionalHazard`` extends the ``hf``
signature with one extra argument named ``covar`` to explicitly tell
users that in its case ``*args`` must have at least one ``covar``
object. The ``*args`` parameter also allows
``model = ProportionalHazard(AFT(AFT(...(Weibull())`` to run, because if
one wants to request ``model.hf``, the number of arguments that must be
passed varies and is spread recursively in the chain of ``baseline``
composition.

However, typing rules can be easily fooled or misrespected if one is not
careful. In the previous example, strictly speaking,
``ProportionalHazard`` overrides the ``hf`` signature and violates the
Liskov Substitution Principle (LSP): ``hf`` expects
``[float, tuple[float, ...]]`` in ``LifetimeModel``, but
``[float, float, tuple[float, ...]]`` in ``ProportionalHazard``.

To handle correct type hinting and avoid issues related to the problem
explained above, ReLife uses ``TypeVarTuple`` introduced in Python 3.11.
This allows ``LifetimeModel`` to act as a
`template <https://en.wikipedia.org/wiki/Template_(C%2B%2B)>`__,
enabling parametric polymorphism and variadic args.

Here is an example of how this can be implemented using
``TypeVarTuple``:

.. code:: python

   VariadicArgs = TypeVarTuple("VariadicArgs")

   class LifetimeModel(Generic[*VariadicArgs]):
       ...
       def hf(self, time: NDArray[np.float64], *args: *VariadicArgs):...

   ModelArgs = tuple[NDArray[np.float64], ...]

   class ProportionalHazard(LifetimeModel[NDArray[np.float64], *ModelArgs]):
       baseline : LifetimeModel[*ModelArgs]
       ...
       def hf(self, time: NDArray[np.float64], covar : NDArray[np.float64], *args: *ModelArgs):...
           return self.covar_effect.g(covar) * self.baseline.hf(time, *args)

In this example, ``VariadicArgs`` is a type variable that can be any
*tuple* of types. Concrete implementation, like ``ProportionalHazard``
can specify the expected *tuple* of types while still maintaining
correct type hinting. Here, ``ProportionalHazard`` expects this tuple of
types as extra arguments :
``tuple[NDArray[np.float64], *ModelArgs] = tuple[NDArray[np.float64], *tuple[NDArray[np.float64], ...]]``
meaning a tuple consisting of at least one ``NDArray[np.float64]`` as
first element followed by zero or more ``NDArray[np.float64]``. Note
that ``tuple[NDArray[np.float64], *tuple[NDArray[np.float64], ...]]``
cannot be rewritten as ``tuple[NDArray[np.float64], ...]`` as it would
mean a tuple consisting of zero or more ``NDArray[np.float64]``.

``LifetimeData`` factory
------------------------

The ``ParametricLifetimeModel`` fitting process uses a ``Likelihood``
object to estimate model parameters. In survival analysis, the
contribution of each observation to the likelihood depends on the type
of lifetime observation (complete, right censored, etc.) and any
truncations. Therefore, it is necessary to parse the data provided by
users and categorize each observation.

To accomplish this task, we use ``LifetimeReader`` objects, which are
responsible for parsing lifetime data. These objects are then used in a
factory object called ``lifetime_data_factory`` to construct a
``LifetimeData`` object. This object encapsulates each group of lifetime
data in an ``IndexedData`` object, which keeps track of the index of the
original data.

``IndexedData`` can be thought of as a simplified version of
``pandas.Series`` that only allows for the intersection or union of data
based. For example, you can use: - ``intersection(*others)`` to get
observations that are left truncated and complete. - ``union(*others)``
to get observations that are complete or right censored.

Additionally, all values of lifetime data are stored as 2D arrays, which
makes probability computations more homogeneous in cases where there are
covariates.

**Why a factory ?** The advantage of using a factory is that it
decouples the process of reading data and creating ``LifetimeData``
objects. This makes it much easier to create variations of the reader
process if needed and isolate code in a cleaner way.

Other considerations
--------------------

There are a few constraints that must be followed when using the
``ParametricModel`` object:

-  At the model level, a user cannot request methods of a model if one
   of the ``params`` values is ``np.nan``. All parameter values must be
   passed at the instantiation or the empty model must be fit before any
   requests are made.
-  At the model level, ``params`` cannot be set individually or by name.
   The user can only set all param values at once using a single setter.
   If a user wants to control ``params`` names, they can use the
   ``params_names`` getter or the string representation of the instance.

Stochastic process sampling
===========================

Suppose we want to sample lifetimes given an ``end_time`` and a sampling
``size``. The first and easiest way to visualize the sampling process is
to consider one asset :

::

   0 1 2 -> samples_index
   -----
   4 2 4 -> it.1
   1 5 2 -> it.2
   2 4 3 -> it.3
   2 . 2 -> it.4
   3 . . -> it.5
   . . . -> StopIteration

As you can see, the sampling generates a sequence of lifetime values per
sample index (here ``size`` = 3). The sequences generated vary in length
depending on whether the cumulative sum of the durations has reached the
time limit (here ``end_time``\ =10).

Sometimes, one wants to generate lifetimes for different assets. In that
case, the number of sequences equals the ``size * nb_assets``

::

   0 0 0 1 1 1 2 2 2 -> samples_index
   0 1 2 0 1 2 0 1 2 -> assets_index
   -----
   4 2 4 2 5 1 2 4 7 -> it.1
   1 5 2 3 6 1 1 4 5 -> it.2
   2 4 3 4 . 8 2 2 . -> it.3
   2 . 2 3 . 4 3 . . -> it.4
   3 . . . . . 1 . . -> it.5
   . . . . . . 5 . . -> it.6
   . . . . . . . . . -> StopIteration

A simple storage of the generated data would be to translate the array
structure shown above in 2d-array, where missing elements are encoded by
``np.nan`` or masked in ``MaskArray``-object. The disadvantage of this
approach is that it can severely overload memory if the number of masked
elements generated becomes very large, as in very large sampling. A
better approach is to store the elements in a compacted 1d-array like
this :

::

   0 0 0 0 0 1 1 1 2 2 2 2 -> samples_index
   -----------------------
   4 1 2 2 3 2 5 4 4 2 3 2

::

   0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 ... -> samples_index
   0 0 0 0 0 1 1 1 2 2 2 2 0 0 0 0 1 1 2 2 2 2 ... -> assets_index
   -----------------------
   4 1 2 2 3 2 5 4 4 2 3 2 2 3 4 3 5 6 1 1 8 4 ...

This format is lighter, but requires some index manipulation to easily
slice on generated data.

Advantages of generator approach
--------------------------------

At a first glimps, used generator approach in ReLife2 only encapsulates
lifetime generation routine in one objet that keeps in memory previous
states without recomputing them many times. It is exactly what basic
while loop did. But, it offers to advantages in comparison to a while
loop :

-  It provides a convenient way to pass other generator routine without
   creating another RenewalProcess class
-  It avoids code duplication (see init_loop and main_loop) : same
   generation, only model changes. First generation has only to send its
   results to main generator

**Solutions**

Lifetime generators are first parametrized with : ``nb_assets``,
``nb_samples``, ``args``. It allows to keep in memory the expected
rvs_size depending on ``nb_assets``,\ ``nb_samples``, ``args``.
Generators also knows ``end_time`` in order to slice uppon valid
lifetime values.

Generators receive an 1d of times then : - it yields variable number of
computed data - update data in an object

one stacks results :

::

   def stacker(*args):
       init = list(args)
       while True:
           new = yield init
           for i, x in enumerate(new):
               init[i] = np.concatenate((init[i], x))


   def generator(..., stacker):
       while True:
           try :
               lifetime = rvs ...
               assets = ...
               stacker.send(lifetime, ...)
           except:
               yield stacker
               stacker.close()
               return
       

``events`` and ``a0``
---------------------

The current implementation has ``events`` and ``a0`` providing data for
``ReplacementPolicyData``, which are used to construct lifetime data in
``to_lifetime_data``. However, this introduces cumbersome code in the
``sample`` functionalities.

-  if model is ``LeftTruncated``, ``a0`` must be catch for
   ``delayed_model`` only and added to generated lifetimes as a
   rectification
-  if model is ``AgeReplacementModel``, ``events`` that represents right
   censoring indicators, is conditionned on ``ar`` values

So, type checking on ``model`` is made combined with ugly numpy slicing
to retrieve correct sampled elements. One can propose easier approach
with generators : why not just writting those data inside the generation
process and not after it was made ?

**Solution :**

Generation process relies on ``rvs`` functionnality of ``LifetimeModel``
objects and ``a0`` is an ``args`` of those model type. We can modify the
``rvs`` function to directly generate rectified lifetimes by
incorporating ``a0``: ``self.baseline(*args, size=size) + a0``. This
way, we no longer need to check for the ``LeftTruncated`` model in the
``sample`` function, as the lifetimes will be correctly generated with
their final values.

Next, we can handle ``events`` more straightforwardly. In the lifetime
generator routine, we can add a check for the model type and generate
``events`` alongside lifetimes, given the ``ar`` values. The
``CountData`` can be updated to include ``events`` data, which is
consistent with the ``ReplacementPolicyData`` interface.

With these modifications, the ``to_lifetime_data`` function no longer
needs to be specific for ``ReplacementPolicyData`` subtypes. Every
``RenewalData`` can have a ``to_lifetime_data`` method, enhancing
coherence and consistency. This approach ensures that every ``sample``
method of both ``RenewalProcess`` and ``Policy`` returns objects that
can be converted to lifetime data.

``sample`` signature and ``args``
---------------------------------

The ``sample`` methods in both ``RenewalProcess`` objects and
``Policy``-like objects (see next example) result in a varying interface
due to the inclusion of ``args``-like parameters. These parameters are
necessary to customize the associated model, reward, and/or discount. I
have identified two possible solutions to this problem:

1. Keep ``sample`` as part of the interface, but encapsulate ``args``
   values in a dictionary of type ``Dict[str, Any]`` during object
   instantiation. The downside of this approach is that users must
   provide each argument value during instantiation, along with
   ``model``, ``reward``, and/or ``discount`` instances.
2. Remove ``sample`` from the interface and make it a standalone
   function (``sample(obj, nb_sample=10, ...)``) or a method within
   another object, such as ``Simulator``.

The second solution, however, still requires varying ``sample``
parametrization depending on the type of object (``obj``) passed as the
first argument. If ``obj`` is a ``RenewalProcess``, ``args`` would
correspond to ``model_args`` and optionally ``delayed_model_args``. If
``obj`` is a ``RunToFailure``, ``args`` would include ``cp``, ``cf``,
``rate``, ``cp1``, and so on. Although this approach could be
implemented using single dispatch from ``functools``, it may not be
user-friendly, as understanding the various parametrization options
would require consulting the documentation.

The first approach could be implemented using a ``Protocol`` to define a
clear and concise ``Policy`` type.\`

.. code:: python

   class Policy(Protocol):
       model: LifetimeModel[*ModelArgs],
       model_args: tuple[*ModelArgs] | tuple[()] = (),
       reward_args : Dict[str, Any],
       nb_assets: int = 1,
       a0: Optional[NDArray[np.float64]] = None,
       delayed_model: LifetimeModel[*DelayedModelArgs],
       delayed_model_args: tuple[*DelayedModelArgs] | tuple[()] = (),

       def expected_total_cost(self, timeline : NDArray[np.float64]) -> NDArray[np.float64]: ...

       def asymptotic_expected_total_cost(self) -> NDArray[np.float64]: ...

       def expected_equivalent_annual_cost(self, timeline : NDArray[np.float64]) -> NDArray[np.float64]: ....

       def asymptotic_expected_equivalent_annual_cost(self) -> NDArray[np.float64]: ...

       def sample(self, nb_samples : int, : float, random_state = None)

       def fit(self): ...

The issue of ``args`` in ``sample`` has been addressed by storing them
as a dictionary of values. Every method will retrieve the required arg
values from this dictionary. From a user’s perspective, every concrete
``Policy`` will explicitly state the names of the ``args`` needed in
``reward_args``. Only the core of the constructor will fill the
dictionary. This attribute could even be a descriptor to automatically
control and convert filled ``args`` values with respect to
``nb_assets``.

One drawback of solution 2 is that it is more aligned with the
object-oriented paradigm and may be less appealing to users who prefer
functional programming. It is true that this approach requires users to
reinstantiate the ``Policy``-like object each time they want to change
``args``. However, this only adds one additional line of code compared
to calling ``sample`` with different arguments. Furthermore, the number
of given args is significant, and it is likely that users would have
already stored them in variables. It is merely a matter of copying and
pasting the relevant variables when reinstantiating the object.

NB : ``Policy`` objects do not need nor ``reward`` or ``discount``
attribute. Discount is always exponential and ``reward`` is implicit.

Lebesgue
========

Many code blocks depend upon ``ls_integrate``, especially in the renewal
package. This method relies on ``support_upper_bound`` and
``support_lower_bound`` properties of model. Because these properties
only exist for ``ls_instagrate`` operations, the ISP and SRP principles
tend to delete them from the ``Model`` interface and delegate their
usage in ``ls_integrate``. As a consequence, ``mrl`` must also be
overridden in derived class where ``support_upper_bound`` is not
``np.inf``.

``ls_integrate`` implementation might vary from one concrete ``Model``
to another. The obvious question is : should ``Model`` interfaces
contain ``ls_integrate`` method. One can say that this operation is only
used to make other operations (moment computation, etc.) and would not
be used by “normal” users. Then, it may be good thing to decouple
``Model`` from ``ls_integrate`` and make ``Model``-objects use
``ls_integrate``. One can also consider ``ls_integrate`` as an usefull
request for advanced mathematical users and no seperate it from
``Model`` interface.

For now, ``ls_integrate`` won’t be seperated from ``Model`` interface
and its base implementation might be overriden in concrete class.

**``func`` argument is a callable that only expects one ``np.ndarray``
as input and return ``np.ndarray`` as output. If one wants to add args,
he must use ``functools.partial``.**

Another problem is that ``ls_integrate`` relied on ``ndim`` argument
which was basically the maximum number of dimension of all array
variables used in the integrated function. It mainly looks at ``*args``
variables but sometimes ``time`` is also a variable in the integrand
(see ``mrl``). To avoid having to specify ndim depending on the variable
shapes at run time, now ``ls_integrate`` automatically convert all
variables in 2d and squeeze the result. This feature is permitted
because variables can’t have more than 2d. Concretely, it uses
``np.atleast_2d`` for both ``args`` and ``integrand`` result.

Lectures
========

-  `Python
   iterator/iterable <https://zestedesavoir.com/tutoriels/954/notions-de-python-avancees/1-starters/2-iterables/>`__
-  `Idem <https://python-patterns.guide/gang-of-four/iterator/>`__
-  Can we use descriptor like Validator attribute (limit validation code
   repeatitions) : read `validator class
   example <https://docs.python.org/3/howto/descriptor.html#validator-class>`__
-  Primer one python iterators : `python doc
   iterators <https://docs.python.org/3/tutorial/classes.html#iterators>`__
-  See functools.reduce to aggregate results of iterator : `python
   functional programming
   style <https://docs.python.org/dev/howto/functional.html#the-functools-module>`__
-  `On difference between iterator and
   iterable <https://stackoverflow.com/questions/9884132/what-are-iterator-iterable-and-iteration>`__
   and `iterable and data
   storage <https://stackoverflow.com/questions/36619152/do-pythons-iterables-really-store-all-values-in-memory>`__
-  Perfect answer on type hinting Iterator `How to write type hinting
   for iterable base
   class <https://stackoverflow.com/questions/73933419/how-to-write-type-hints-for-an-iterable-abstract-base-class>`__
-  On functional programming and partial function : `partial functions
   python <https://chriskiehl.com/article/Cleaner-coding-through-partially-applied-functions>`__
