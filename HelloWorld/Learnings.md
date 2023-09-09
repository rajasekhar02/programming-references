## [Course Refered](https://github.com/mike-north/ts-fundamentals-v3)

## TIPS

**TIPS 1**: Using unknown instead of any to prevent from lint errors

**TIPS 2**: Thinking an Array as Object also helpful in resolving types

**TIPS 3**: Using Recursion to loop over the types

**TIPS 4**: Using infer to create type variables

**TIPS 5**: To iterate on string use template literals operator(\`\`)

## TS Files

A good way to think of TS files:

- .ts files contain both type information and code that runs
- .js files contain only code that runs
- .d.ts files contain only type information

## Categorizing Type Systems

### Static vs dynamic

- TypeScript’s type system is static.
- Dynamic type systems perform their “type equivalence” evaluation at runtime.

### Nominal vs structural

- Nominal type systems are all about NAMES.

  ```Java
  public class Car {
  String make;
  String model;
  int make;
  }
  public class CarChecker {
  // takes a `Car` argument, returns a `String`
  public static String printCar(Car car) {  }
  }
  Car myCar = new Car();
  // TYPE CHECKING
  // -------------
  // Is `myCar` type-equivalent to
  //     what `checkCar` wants as an argument?
  CarChecker.checkCar(myCar);
  ```

  In the code above, when considering the question of type equivalence on the last line, all that matters is whether myCar is an instance of the class named Car.

- Structural type systems are all about STRUCTURE or SHAPE. Let’s look at a TypeScript example:

```ts
class Car {
  make: string;
  model: string;
  year: number;
  isElectric: boolean;
}

class Truck {
  make: string;
  model: string;
  year: number;
  towingCapacity: number;
}

const vehicle = {
  make: "Honda",
  model: "Accord",
  year: 2017
};

function printCar(car: { make: string; model: string; year: number }) {
  console.log(`${car.make} ${car.model} (${car.year})`);
}

printCar(new Car()); // Fine
printCar(new Truck()); // Fine
printCar(vehicle); // Fine
```

The function printCar doesn’t care about which constructor its argument came from, it only cares about whether it has:

A make property that’s of type string
A model property that’s of type string
A year property that’s of type number
If the argument passed to it meets these requirements, printCar is happy.

## Compiler options

### [target](https://www.typescriptlang.org/tsconfig#target)

Modern browsers support all ES6 features, so ES6 is a good choice. You might choose to set a lower target if your code is deployed to older environments, or a higher target if your code is guaranteed to run in newer environments.

---

### [module](https://www.typescriptlang.org/tsconfig#module)

Sets the module system for the program. See the [Modules](https://www.typescriptlang.org/docs/handbook/modules.html) reference page for more information. You very likely want "CommonJS" for node projects.

---

### declaration

Generate .d.ts files for every TypeScript or JavaScript file inside your project. These .d.ts files are type definition files which describe the external API of your module. With .d.ts files, tools like TypeScript can provide intellisense and accurate types for un-typed code.

---

## Type Aliases

Type aliases help to address this, by allowing us to:

- define a more meaningful name for this type
- declare the particulars of the type in a single place
- import and export this type from modules, the same as if it were an exported value

### Inheritance in type aliases

You can create type aliases that combine existing types with new behavior by using Intersection (`&`) types.

## Interfaces

- An interface is a way of defining an object type. An “object type” can be thought of as, “an instance of a class could conceivably look like this”.
  For example, `string | number` is not an object type, because it makes use of the union type operator.
- Like type aliases, interfaces can be imported/exported between modules just like values, and they serve to provide a “name” for a specific type.

### Inheritance in interfaces

`extends` is used in following cases:

- a subclass extends from a base class.
- a “sub-interface” extends from a base interface

`implements` in TypeScript adds a second heritage clause that can be used to state that a given class should produce instances that confirm to a given interface.

- While TypeScript (and JavaScript) does not support true multiple inheritance (extending from more than one base class), this implements keyword gives us the ability to validate, at compile time, that instances of a class conform to one or more “contracts” (types).

- While it’s possible to use implements with a type alias, if the type ever breaks the “object type” rules there’s some potential for problems…

```ts
type CanBark =
  | number
  | {
      bark(): string;
    };

class Dog implements CanBark {
  // ERROR: A class can only implement an object type or intersection of object types with statically known members.
  bark() {
    return "woof";
  }
  eat(food) {
    consumeFood(food);
  }
}
```

For this reason, it is best to use interfaces for types that are used with the implements heritage clause.

- TypeScript interfaces are “open”, meaning that unlike in type aliases, you can have multiple declarations in the same scope:

```ts
interface AnimalLike {
  isAlive(): boolean;
}
function feed(animal: AnimalLike) {
  animal.eat;

  animal.isAlive;
}

// SECOND DECLARATION OF THE SAME NAME
interface AnimalLike {
  eat(food): void;
}
```

These declarations are merged together to create a result identical to what you would see if both the isAlive and eat methods were on a single interface declaration.

### Choosing which to use

In many situations, either a type alias or an interface would be perfectly fine, however…

- If you need to define something other than an object type (e.g., use of the | union type operator), you must use a type alias
- If you need to define a type to use with the implements heritage term, it’s best to use an interface
- If you need to allow consumers of your types to augment them, you must use an interface.

### Recursion

Recursive types, are self-referential, and are often used to describe infinitely nestable types. For example, consider infinitely nestable arrays of numbers

```ts
type NestedNumbers = number | NestedNumbers[];

const val: NestedNumbers = [3, 4, [5, 6, [7], 59], 221];

if (typeof val !== "number") {
  val.push(41);
  // Below Line ERROR: Argument of type 'string' is not assignable to parameter of type 'NestedNumbers'.
  val.push("this will not work");
}
```

## Functions

`void` is a special type, that’s specifically used to describe function return values. It has the following meaning:

`The return value of a void function is intended to be ignored`

### Constructor Signatures

Construct signatures are similar to call signatures, except they describe what should happen with the new keyword.

```ts
interface DateConstructor {
  new (value: number): Date;
}

let MyDateConstructor: DateConstructor = Date;
const d = new MyDateConstructor();
```

### Function overloads

- There should be a declaration followed after the overloading function definition
- All the overloaded functions should be exported

### Function type best practices

- Explicitly define return types

## Classes

- JS Classes private fields are followed #. `#fields`
- `readonly`: While not strictly an access modifier keyword (because it has nothing to do with visibility), TypeScript provides a readonly keyword that can be used with class fields.
- Note the following order of what ends up in the class constructor:

  - super()
  - param property initialization
  - other class field initialization
  - anything else that was in your constructor after super()
  - Also note that, while it is possible in JS to put stuff before super(), the use of class field initializers or param properties disallows this:

```js
class Base {}

class Car extends Base {
  foo = console.log("class field initializer")
  constructor(public make: string) {
    console.log("before super")
    super()
    console.log("custom constructor stuff")
  }
}

const c = new Car("honda")
```

## Top and Bottom Types

### Top Types

`any`: You can think of values with an any type as “playing by the usual JavaScript rules”.
`unknown`: unknown is different from any in a very important way, i.e: Values with an unknown type cannot be used without first applying a type guard

```ts
// ERROR: Accessing `myUnknown.it.is.possible.to.access.any.deep.property` Object is of type 'unknown'.
let myUnknown: unknown = 14;

// Correct Way: Using Type guard
// This code runs for { myUnknown| anything }
if (typeof myUnknown === "string") {
  // This code runs for { myUnknown| all strings }
  console.log(myUnknown, "is a string");

  let myUnknown: string;
} else if (typeof myUnknown === "number") {
  // This code runs for { myUnknown| all numbers }
  console.log(myUnknown, "is a number");

  let myUnknown: number;
} else {
  // this would run for "the leftovers"
  //       { myUnknown| anything except string or numbers }
}
```

**Practical use of top types:**

- if you ever convert a project from JavaScript to TypeScript, it’s very convenient to be able to incrementally add increasingly strong types.
- `unknown` is great for values received at runtime (e.g., your data layer). By obligating consumers of these values to perform some light validation before using them, errors are caught earlier, and can often be surfaced with more context.

### Bottom Type

[`never`](https://www.typescript-training.com/course/fundamentals-v3/11-top-and-bottom-types/#exhaustive-conditionals): approach works nicely with a switch statement, when the UnreachableError is thrown from the default case clause.

## Type Guards

### Built-in typeguards

Refer to `typeguards.ts`

### [User-defined type guards](https://www.typescript-training.com/course/fundamentals-v3/12-type-guards/#writing-high-quality-guards)

**value is Foo**

The first kind of user-defined type guard we will review is an is type guard. It is perfectly suited for our example above because it’s meant to work in cooperation with a control flow statement of some sort, to indicate that different branches of the “flow” will be taken based on an evaluation of valueToTest’s type. Pay very close attention to isCarLike’s return type

```ts
interface CarLike {
  make: string;
  model: string;
  year: number;
}

let maybeCar: unknown;

// the guard
function isCarLike(valueToTest: any): valueToTest is CarLike {
  return (
    valueToTest &&
    typeof valueToTest === "object" &&
    "make" in valueToTest &&
    typeof valueToTest["make"] === "string" &&
    "model" in valueToTest &&
    typeof valueToTest["model"] === "string" &&
    "year" in valueToTest &&
    typeof valueToTest["year"] === "number"
  );
}

// using the guard
if (isCarLike(maybeCar)) {
  maybeCar;
  // Typehint: let maybeCar: CarLike
}
```

**asserts value is Foo**

There is another approach we could take that eliminates the need for a conditional. Pay very close attention to assertsIsCarLike’s return type:

```ts
interface CarLike {
  make: string;
  model: string;
  year: number;
}

let maybeCar: unknown;

// the guard
function assertsIsCarLike(valueToTest: any): asserts valueToTest is CarLike {
  if (
    !(
      valueToTest &&
      typeof valueToTest === "object" &&
      "make" in valueToTest &&
      typeof valueToTest["make"] === "string" &&
      "model" in valueToTest &&
      typeof valueToTest["model"] === "string" &&
      "year" in valueToTest &&
      typeof valueToTest["year"] === "number"
    )
  )
    throw new Error(`Value does not appear to be a CarLike${valueToTest}`);
}

// using the guard
maybeCar;

let maybeCar: unknown;
assertsIsCarLike(maybeCar);
maybeCar;
// Typehint: let maybeCar: CarLike
```

## Nullish Values

Although null, void and undefined are all used to describe “nothing” or “empty”, they are independent types in TypeScript. Learning to use them to your advantage, and they can be powerful tools for clearly expressing your intent as a code author.

### null

`null` means: there is a value, and that value is nothing.

This nothing is very much a defined value, and is certainly a presence — not an absence — of information.

```ts
const userInfo = {
  name: "Mike",
  email: "mike@example.com",
  secondaryEmail: null // user has no secondary email
};
```

### undefined

- `undefined` means the value isn’t available (yet?)
- `undefined` is an unambiguous indication that there may be something different there in the future

```ts
const formInProgress = {
  createdAt: new Date(),
  data: new FormData(),
  completedAt: undefined //
};
function submitForm() {
  formInProgress.completedAt = new Date();
}
```

### void

`void` should exclusively be used to describe that a function’s return value should be ignored

### Non-null assertion operator

- The non-null assertion operator (!.) is used to cast away the possibility that a value might be null or undefined.

- If the value does turn out to be missing, you will get the familiar `cannot call foo on undefined family of errors at runtime`

- It is recommend against using this in your app or library code, but if your test infrastructure represents a throw as a test failure (most should) this is a great type guard to use in your test suite.

### Definite assignment operator

- The definite assignment !: operator is used to suppress TypeScript’s objections about a class field being used, when it can’t be `proven (means, “the compiler can’t convince itself.”)` that it was initialized.
- There is a good example `(file: nullish.ts)` of a totally appropriate use of the definite assignment operator, where I as the code author have some extra context that the compiler does not.

## Generics

### Generics Scopes and Constraints

**Generic Constraints**

- Generic constraints allow us to describe the “minimum requirement” for a type param, such that we can achieve a high degree of flexibility, while still being able to safely assume some minimal structure and behavior.

```diff
- function listToDict(list: HasId[]): Dict<HasId> {
+ function listToDict<T extends HasId>(list: T[]): Dict<T> {
```

- When a class extends from a base class, it’s guaranteed to at least align with the base class structure. In the same way, T extends HasId guarantees that “T is at least a HasId”

## Declaration Merging

### Stacking multiple things on a identifier

We can use the same variable for class, namespace and interface. The compiler use the identifies the correct type based on the variable usage.

```ts
class Fruit {
  static createBanana(): Fruit {
    return { name: "banana", color: "yellow", mass: 183 };
  }
}

// the namespace
namespace Fruit {
  function createFruit(): Fruit {
    // the type
    return Fruit.createBanana(); // the class
  }
}

interface Fruit {
  name: string;
  mass: number;
  color: string;
}

export { Fruit };
```

```ts
const is_a_value = 4;
type is_a_type = {};
namespace is_a_namespace {
  const foo = 17;
}

// how to test for a value
const x = is_a_value; // the value position (RHS of =).

// how to test for a type
const y: is_a_type = {}; // the type position (LHS of = ).

// how to test for a namespace (hover over is_a_namespace symbol)
is_a_namespace;
```

### A look back on class

classes are both a type and a value.

```ts
class Fruit {
  name?: string;
  mass?: number;
  color?: string;
  static createBanana(): Fruit {
    return { name: "banana", color: "yellow", mass: 183 };
  }
}

// how to test for a value
const valueTest = Fruit; // Fruit is a value!
valueTest.createBanana;

// how to test for a type
let typeTest: Fruit = {} as any; // Fruit is a type!
typeTest.color;
```

The word completions for the letter c above are a clue as to what’s going on:

- When Fruit is used as a type, it describes the type of an instance of Fruit
- When Fruit is used as a value, it can both act as the constructor (e.g., new Fruit()) and holds the “static side” of the class (createBanana() in this case)

## Modules and CJS Interop

### ES Module imports and exports

```ts
// named imports
import { strawberry, raspberry } from "./berries";
import kiwi from "./kiwi"; // default import
export function makeFruitSalad() {} // named export
export default class FruitBasket {} // default export
export { lemon, lime } from "./citrus";
```

### CommonJS Interop

Most of the time, you can just convert something like

```ts
const fs = require("fs");
```

into

```ts
// namespace import
import \* as fs from "fs"
```

but occasionally, you’ll run into a rare situation where the CJS module you’re importing from, exports a single thing that’s incompatible with this namespace import technique. For Example as below

```ts
////////////////////////////////////////////////////////
// @filename: fruits.ts
function createBanana() {
  return { name: "banana", color: "yellow", mass: 183 };
}

// equivalent to CJS `module.exports = createBanana`
export = createBanana;
////////////////////////////////////////////////////////
// @filename: smoothie.ts

import * as createBanana from "./fruits";
```

In these cases simply import using CJS module system

```ts
////////////////////////////////////////////////////////
// @filename: fruits.ts
function createBanana() {
  return { name: "banana", color: "yellow", mass: 183 };
}

// equivalent to CJS `module.exports = createBanana`
export = createBanana;
////////////////////////////////////////////////////////
// @filename: smoothie.ts

import createBanana = require("./fruits");
const banana = createBanana();
```

### Importing non-TS things

Particularly if you use a bundler like webpack, parcel or snowpack, you may end up importing things that aren’t `.js` or `.ts` files

```ts
import img from "./file.png";
```

`file.png` is obviously not a TypeScript file — we just need to tell TypeScript that whenever we import a `.png` file, it should be treated as if it’s a JS module with a string value as its default export

This can be accomplished through a module declaration as shown below

```ts
// @filename: global.d.ts
declare module "*.png" {
  const imgUrl: string;
  export default imgUrl;
}
// @filename: component.ts
import img from "./file.png";
```

## Type Queries

### keyof

The `keyof` type query allows us to obtain `a type` that represents all property keys on a given interface

### typeof

The typeof type query allows you to extract a type from a value.

## Conditional Types

### Syntax

```ts
type CookingDevice<T> = T extends "grill" ? Grill : Oven;
```

### Example

```ts
class Grill {
  startGas() {}
  stopGas() {}
}
class Oven {
  setTemperature(degrees: number) {}
}

type CookingDevice<T> = T extends "grill" ? Grill : Oven;

let device1: CookingDevice<"grill">; // device1 Type is Grill

let device2: CookingDevice<"oven">; // device2 Type is Oven
```

### [Inferring within conditional types](https://www.typescriptlang.org/docs/handbook/2/conditional-types.html#inferring-within-conditional-types)

In the same release where conditional types were added to TypeScript a new `infer` keyword was added as well. This keyword, which can only be used in the context of a condition expression (within a conditional type declaration) is an important tool for being able to extract out pieces of type information from other types.

```ts
// Syntax
type Flatten<Type> = Type extends Array<infer Item> ? Item : Type;
```

### [Distributive Conditional Types](https://www.typescriptlang.org/docs/handbook/2/conditional-types.html#distributive-conditional-types)

When conditional types act on a generic type, they become distributive when given a union type.

```ts
type ToArray<Type> = Type extends any ? Type[] : never;
//    ^?
```

```ts
type ToArray<Type> = Type extends any ? Type[] : never;

type StrArrOrNumArr = ToArray<string | number>; // Finally type StrArrOrNumArr = string[] | number[]
```

## Indexed Access Types

```ts
interface Car {
  make: string;
  model: string;
  year: number;
  color: {
    red: string;
    green: string;
    blue: string;
  };
}

let carColor: Car["color"];
/*Type of carColor is {
    red: string;
    green: string;
    blue: string;
}*/

// deeper into the object through multiple “accesses”
let carColorRedComponent: Car["color"]["red"];

// Can pass or “project” a union type (|) through Car as an index, as long as all parts of the union type are each a valid index
let carProperty: Car["color" | "year"];
```

## Mapped Types

The use of the `in` keyword typescript compiler allows the generic type `OptionsFlags` to iterate over all the properties (keys) in the provided type `Type`, enabling the creation of a new type `FeatureOptions` with `boolean` flags for each property, effectively representing options for various features.

```ts
type OptionsFlags<Type> = {
  [Property in keyof Type]: boolean;
};

type Features = {
  darkMode: () => void;
  newUserProfile: () => void;
};

type FeatureOptions = OptionsFlags<Features>;
/*      ^^
type FeatureOptions = {
    darkMode: boolean;
    newUserProfile: boolean;
}
*/
```

### [Mapping Modifiers](https://www.typescriptlang.org/docs/handbook/2/mapped-types.html#mapping-modifiers)

There are two additional modifiers which can be applied during mapping: readonly and ? which affect mutability and optionality respectively.

You can remove or add these modifiers by prefixing with - or +. If you don’t add a prefix, then + is assumed.

### Key Remapping via as

```ts
type MappedTypeWithNewProperties<Type> = {
  [Properties in keyof Type as NewKeyType]: Type[Properties];
};
```