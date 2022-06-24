# Risp (in (Rust) (Lisp))


Many years ago, Peter Norvig wrote a beautiful article [about creating a lisp
interpreter in Python](http://norvig.com/lispy.html). It’s the most fun
tutorial I’ve seen, not just because it teaches you about my favorite language
family (Lisp), but because it cuts through to the essence of interpreters, is
fun to follow and quick to finish.

Recently, I had some time and wanted to learn Rust. It’s a beautiful systems
language, and I’ve seen some great work come out from those who adopt it. I
thought, _what better way to learn Rust, than to create a lisp interpreter in
it?_

 **Hence, Risp — a lisp in rust — was born.** In this essay you and I will
follow along with [Norvig’s Lispy](http://norvig.com/lispy.html), but instead
of Python, we’ll do it in Rust 🙂.

## Syntax, Semantics and Notes on Following Along

If you haven’t heard of lisp, some Paul Graham’s essays
([one](http://www.paulgraham.com/progbot.html),
[two](http://www.paulgraham.com/diff.html),
[three](http://www.paulgraham.com/avg.html)), alongside some [Rich Hickey
talks](https://m.stopa.io/favorite-rich-hickey-talks-6bcb23da6ff2) will get
you fired up. In short, everything is a list, everything is an expression, and
that makes for a very powerful language.

Our structure will be similar to Norvig’s tutorial, though I depart slightly
in two ways:

  1. Instead of 2 stopping points (Lispy Calculator and Full Lispy), we have 4 stopping points. This reflects the phases I took to build it in Rust.
  2. Norvig’s syntax is based on Scheme. We will base it on Scheme too, but since I’m also a Clojure fan, I sometimes used slightly different naming, and different implementations for a few functions. I will note when I do that in the essay.

Finally, this is the first program I wrote in Rust. I may have misused some
things, so if you’re a Rust hacker, I’d love to hear your feedback 🙂.

With the notes out of the way, let’s get into it.

## Language 1: _Just a Risp calculator_

As Norvig suggests, our first goal is to create a subset of lisp, that can do
what a basic calculator can do.

To make it as simple as possible to follow, for language 1, **we’ll _only_
support addition and subtraction.** No variable definitions, no if statements,
nada.

This departs a bit from Lispy, but I found this stopping point a lot more
convenient when writing it in Rust. So, our goal:

[code]

    (+ 10 5 2)//=> 17
    (- 10 5 2) //=> 3
[/code]

The important process we need to remember is the flow of an interpreter:

 _our program_ ⟶ _**parse**_ ⟶ _abstract syntax tree_ ⟶ _**eval**_ ⟶ _result_

We will need to **parse** our program and convert it into an abstract syntax
tree. After that, we can **eval** the abstract syntax tree and get our result.
(Refer to Norvig’s article for more detailed definitions and explanations).

### Type Definitions

Risp can have three kinds of values for now:

[code]

    #[derive(Clone)]
    enum RispExp {
      Symbol(String),
      Number(f64),
      List(Vec<RispExp>),
    } 
[/code]

We’ll also need an error type. We’ll keep this simple, but if you’re curious
there _is_ a [more robust
approach](https://news.ycombinator.com/item?id=19812159).

[code]

    #[derive(Debug)]
    enum RispErr {
      Reason(String),
    }
[/code]

Finally, we’ll need an _environment_ type. This is where we will store defined
variables, built-in functions, and so forth:

[code]

    #[derive(Clone)]
    struct RispEnv {
      data: HashMap<String, RispExp>,
    }
[/code]

### Parsing

Our goal is to take our program, and build an abstract syntax tree from it.
For us, that is going to be a `RispExp`. To do this, first we will take our
program, and cut it up into a bunch of tokens:

[code]

    tokenize("(+ 10 5)") //=> ["(", "+", "10", "5", ")"]
[/code]

Here’s how we can do that in Rust:

[code]

    fn tokenize(expr: String) -> Vec<String> {
      expr
        .replace("(", " ( ")
        .replace(")", " ) ")
        .split_whitespace()
        .map(|x| x.to_string())
        .collect()
    }
[/code]

Then, we can parse these tokens, into a `RispExp`:

[code]

    fn parse<'a>(tokens: &'a [String]) -> Result<(RispExp, &'a [String]), RispErr> {
      let (token, rest) = tokens.split_first()
        .ok_or(
          RispErr::Reason("could not get token".to_string())
        )?;
      match &token[..] {
        "(" => read_seq(rest),
        ")" => Err(RispErr::Reason("unexpected `)`".to_string())),
        _ => Ok((parse_atom(token), rest)),
      }
    }
[/code]

 ** _Note:_** _I depart slightly from Norvig’s implementation, by returning
the “next” slice. This lets us recurse and parse nested lists, without
mutating the original list._

We get the token for the current position. If it’s the beginning of a list
“(“, we start reading and parsing the tokens that follow, until we hit a
closing parenthesis:

[code]

    fn read_seq<'a>(tokens: &'a [String]) -> Result<(RispExp, &'a [String]), RispErr> {
      let mut res: Vec<RispExp> = vec![];
      let mut xs = tokens;
      loop {
        let (next_token, rest) = xs
          .split_first()
          .ok_or(RispErr::Reason("could not find closing `)`".to_string()))
          ?;
        if next_token == ")" {
          return Ok((RispExp::List(res), rest)) // skip `)`, head to the token after
        }
        let (exp, new_xs) = parse(&xs)?;
        res.push(exp);
        xs = new_xs;
      }
    }
[/code]

If it’s a closing tag of a list “)”, we return an error, as read_seq should
have skipped past it.

Otherwise, it can only be an atom, so we parse that:

[code]

    fn parse_atom(token: &str) -> RispExp {      
      let potential_float: Result<f64, ParseFloatError> = token.parse();
      match potential_float {
        Ok(v) => RispExp::Number(v),
        Err(_) => RispExp::Symbol(token.to_string().clone())
      }
    }
[/code]

### Environment

Let’s go ahead and create the default, global environment. As Norvig explains,
environments are where we will store variable definitions and built-in
functions.

To implement built-in operations `(+, -)`, we need a way to save rust function
references. Let’s update `RispExp`, so that we can store rust function
references:

[code]

    #[derive(Clone)]
    enum RispExp {
      Symbol(String),
      Number(f64),
      List(Vec<RispExp>),
      Func(fn(&[RispExp]) -> Result<RispExp, RispErr>), // bam
    }
[/code]

Then, we can create a `default_env` function, that returns a `RispEnv`, which
implements +, and -

[code]

    fn default_env() -> RispEnv {
      let mut data: HashMap<String, RispExp> = HashMap::new();
      data.insert(
        "+".to_string(), 
        RispExp::Func(
          |args: &[RispExp]| -> Result<RispExp, RispErr> {
            let sum = parse_list_of_floats(args)?.iter().fold(0.0, |sum, a| sum + a);
            
            Ok(RispExp::Number(sum))
          }
        )
      );
      data.insert(
        "-".to_string(), 
        RispExp::Func(
          |args: &[RispExp]| -> Result<RispExp, RispErr> {
            let floats = parse_list_of_floats(args)?;
            let first = *floats.first().ok_or(RispErr::Reason("expected at least one number".to_string()))?;
            let sum_of_rest = floats[1..].iter().fold(0.0, |sum, a| sum + a);
            
            Ok(RispExp::Number(first - sum_of_rest))
          }
        )
      );
      
      RispEnv {data}
    }
[/code]

 ** _Note:_** _I am following Clojure’s spec for + and -._

To make this simpler, I made a quick helper, which enforces that all `RispExp`
that we receive are floats:

[code]

    fn parse_list_of_floats(args: &[RispExp]) -> Result<Vec<f64>, RispErr> {
      args
        .iter()
        .map(|x| parse_single_float(x))
        .collect()
    }
    
    fn parse_single_float(exp: &RispExp) -> Result<f64, RispErr> {
      match exp {
        RispExp::Number(num) => Ok(*num),
        _ => Err(RispErr::Reason("expected a number".to_string())),
      }
    }
[/code]

### Evaluation

Now, time to implement **eval.**

If it’s a symbol, we’ll query for that symbol in the environment and return it
(for now, it should be a `RispExp::Func`)

If it’s a number, we’ll simply return it.

If it’s a list, we’ll evaluate the first form. It should be a `RispExp::Func`.
Then, we’ll call that function with all the other evaluated forms as the
arguments.

[code]

    fn eval(exp: &RispExp, env: &mut RispEnv) -> Result<RispExp, RispErr> {
      match exp {
        RispExp::Symbol(k) =>
            env.data.get(k)
            .ok_or(
              RispErr::Reason(
                format!("unexpected symbol k='{}'", k)
              )
            )
            .map(|x| x.clone())
        ,
        RispExp::Number(_a) => Ok(exp.clone()),
        RispExp::List(list) => {
          let first_form = list
            .first()
            .ok_or(RispErr::Reason("expected a non-empty list".to_string()))?;
          let arg_forms = &list[1..];
          let first_eval = eval(first_form, env)?;
          match first_eval {
            RispExp::Func(f) => {
              let args_eval = arg_forms
                .iter()
                .map(|x| eval(x, env))
                .collect::<Result<Vec<RispExp>, RispErr>>();
              f(&args_eval?)
            },
            _ => Err(
              RispErr::Reason("first form must be a function".to_string())
            ),
          }
        },
        RispExp::Func(_) => Err(
          RispErr::Reason("unexpected form".to_string())
        ),
      }
    }
[/code]

 **Aand, bam, we have eval.**

### Repl

Now, to make this fun and interactive, let’s make a repl.

We first need a way to convert our `RispExp` to a string. Let’s implement the
`Display` trait

[code]

    impl fmt::Display for RispExp {
      fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let str = match self {
          RispExp::Symbol(s) => s.clone(),
          RispExp::Number(n) => n.to_string(),
          RispExp::List(list) => {
            let xs: Vec<String> = list
              .iter()
              .map(|x| x.to_string())
              .collect();
            format!("({})", xs.join(","))
          },
          RispExp::Func(_) => "Function {}".to_string(),
        };
        
        write!(f, "{}", str)
      }
    }
[/code]

Then, let’s tie the interpreter process into a loop

[code]

    fn parse_eval(expr: String, env: &mut RispEnv) -> Result<RispExp, RispErr> {
      let (parsed_exp, _) = parse(&tokenize(expr))?;
      let evaled_exp = eval(&parsed_exp, env)?;
      
      Ok(evaled_exp)
    }
    
    fn slurp_expr() -> String {
      let mut expr = String::new();
      
      io::stdin().read_line(&mut expr)
        .expect("Failed to read line");
      
      expr
    }
    
    fn main() {
      let env = &mut default_env();
      loop {
        println!("risp >");
        let expr = slurp_expr();
        match parse_eval(expr, env) {
          Ok(res) => println!("// 🔥 => {}", res),
          Err(e) => match e {
            RispErr::Reason(msg) => println!("// 🙀 => {}", msg),
          },
        }
      }
    }
[/code]

### Aand, voila, language 1.0 is done. [Here’s the code so
far](https://gist.github.com/stopachka/22b4b06b8263687d7178f61fb22e1bf2) 🙂

We can now add and subtract!

[code]

    risp >
    (+ 10 5 (- 10 3 3))
    // 🔥 => 19
[/code]

## Language 1.1: Risp calculator++

Okay, we have a basic calculator. Now, let’s add support for booleans, and
introduce some equality comparators.

To implement bools, let’s include it in our `RispExp`

[code]

    #[derive(Clone)]
    enum RispExp {
      Bool(bool), // bam
      Symbol(String),
      Number(f64),
      List(Vec<RispExp>),
      Func(fn(&[RispExp]) -> Result<RispExp, RispErr>),
    }
[/code]

Rust will tell us to update `Display`

[code]

    impl fmt::Display for RispExp {
      fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let str = match self {
          RispExp::Bool(a) => a.to_string(),
[/code]

Then Rust will tell us we should change `eval`, to consider bools:

[code]

    fn eval(exp: &RispExp, env: &mut RispEnv) -> Result<RispExp, RispErr> {
      match exp {
        ...
        RispExp::Bool(_a) => Ok(exp.clone()),
[/code]

Let’s also update our `parse_atom` function, to consider bools:

[code]

    fn parse_atom(token: &str) -> RispExp {
      match token.as_ref() {
        "true" => RispExp::Bool(true),
        "false" => RispExp::Bool(false),
        _ => {
          let potential_float: Result<f64, ParseFloatError> = token.parse();
          match potential_float {
            Ok(v) => RispExp::Number(v),
            Err(_) => RispExp::Symbol(token.to_string().clone())
          }
        }
      }
    }
[/code]

Now, we _should_ be good to go. To really see these in action though, let’s
implement `=, >, <, >=, <=`

### Comparison Operators

In clojure, these comparison operators are a bit special. They can take more
than 2 args, and return true if they are in a monotonic order that satisfies
the operator.

For example `(> 6 5 3 2)` is true, because 6 > 5 > 3 > 2\. Let’s do this for
Risp:

[code]

    fn default_env() -> RispEnv {
      let mut data: HashMap<String, RispExp> = HashMap::new();
      ...
      data.insert(
        "=".to_string(), 
        RispExp::Func(ensure_tonicity!(|a, b| a == b))
      );
      data.insert(
        ">".to_string(), 
        RispExp::Func(ensure_tonicity!(|a, b| a > b))
      );
      data.insert(
        ">=".to_string(), 
        RispExp::Func(ensure_tonicity!(|a, b| a >= b))
      );
      data.insert(
        "<".to_string(), 
        RispExp::Func(ensure_tonicity!(|a, b| a < b))
      );
      data.insert(
        "<=".to_string(), 
        RispExp::Func(ensure_tonicity!(|a, b| a <= b))
      );
      
      RispEnv {data}
    }
[/code]

The key here is our helper macro `ensure_tonicity`. This takes a checker
function, and ensures that the conditional passes in a monotonic way.

[code]

    macro_rules! ensure_tonicity {
      ($check_fn:expr) => {{
        |args: &[RispExp]| -> Result<RispExp, RispErr> {
          let floats = parse_list_of_floats(args)?;
          let first = floats.first().ok_or(RispErr::Reason("expected at least one number".to_string()))?;
          let rest = &floats[1..];
          fn f (prev: &f64, xs: &[f64]) -> bool {
            match xs.first() {
              Some(x) => $check_fn(prev, x) && f(x, &xs[1..]),
              None => true,
            }
          };
          Ok(RispExp::Bool(f(first, rest)))
        }
      }};
    }
[/code]

### Aand, voila, language 1.1 is done. [Here’s the code so
far](https://gist.github.com/stopachka/ddedb35ca7fc9ea5dd320c218e9054c8) 🙂

We can now use comparators, and see booleans!

[code]

    risp >
    (> 6 4 3 1)
    // 🔥 => true
[/code]

## Language 1.2: Almost Risp

Okay, now, let’s make this a _language._ Let’s introduce `def` and `if`.

To do this, let’s update `eval` to deal with built-in operators:

[code]

    fn eval(exp: &RispExp, env: &mut RispEnv) -> Result<RispExp, RispErr> {
      match exp {
        ...
        RispExp::List(list) => {
          let first_form = list
            .first()
            .ok_or(RispErr::Reason("expected a non-empty list".to_string()))?;
          let arg_forms = &list[1..];
          match eval_built_in_form(first_form, arg_forms, env) {
            Some(res) => res,
            None => {
              let first_eval = eval(first_form, env)?;
              match first_eval {
                RispExp::Func(f) => {
                  let args_eval = arg_forms
                    .iter()
                    .map(|x| eval(x, env))
                    .collect::<Result<Vec<RispExp>, RispErr>>();
                  return f(&args_eval?);
                },
                _ => Err(
                  RispErr::Reason("first form must be a function".to_string())
                ),
              }
            }
          }
        },
[/code]

We take the first form, and try to eval it as a built-in. If we can, voila,
otherwise we evaluate as normal.

Here’s how `eval_built_in_form` looks:

[code]

    fn eval_built_in_form(
      exp: &RispExp, arg_forms: &[RispExp], env: &mut RispEnv
    ) -> Option<Result<RispExp, RispErr>> {
      match exp {
        RispExp::Symbol(s) => 
          match s.as_ref() {
            "if" => Some(eval_if_args(arg_forms, env)),
            "def" => Some(eval_def_args(arg_forms, env)),
            _ => None,
          }
        ,
        _ => None,
      }
    }
[/code]

### if

Here’s how we can implement if:

[code]

    fn eval_if_args(arg_forms: &[RispExp], env: &mut RispEnv) -> Result<RispExp, RispErr> {
      let test_form = arg_forms.first().ok_or(
        RispErr::Reason(
          "expected test form".to_string(),
        )
      )?;
      let test_eval = eval(test_form, env)?;
      match test_eval {
        RispExp::Bool(b) => {
          let form_idx = if b { 1 } else { 2 };
          let res_form = arg_forms.get(form_idx)
            .ok_or(RispErr::Reason(
              format!("expected form idx={}", form_idx)
            ))?;
          let res_eval = eval(res_form, env);
          
          res_eval
        },
        _ => Err(
          RispErr::Reason(format!("unexpected test form='{}'", test_form.to_string()))
        )
      }
    }
[/code]

### def

And here’s def:

[code]

    fn eval_def_args(arg_forms: &[RispExp], env: &mut RispEnv) -> Result<RispExp, RispErr> {
      let first_form = arg_forms.first().ok_or(
        RispErr::Reason(
          "expected first form".to_string(),
        )
      )?;
      let first_str = match first_form {
        RispExp::Symbol(s) => Ok(s.clone()),
        _ => Err(RispErr::Reason(
          "expected first form to be a symbol".to_string(),
        ))
      }?;
      let second_form = arg_forms.get(1).ok_or(
        RispErr::Reason(
          "expected second form".to_string(),
        )
      )?;
      if arg_forms.len() > 2 {
        return Err(
          RispErr::Reason(
            "def can only have two forms ".to_string(),
          )
        )
      } 
      let second_eval = eval(second_form, env)?;
      env.data.insert(first_str, second_eval);
      
      Ok(first_form.clone())
    }
[/code]

### Aand bam, language 1.2 is done. [Here’s the code so
far](https://gist.github.com/stopachka/b862ed8ee719d8532f5c5cdb1bd2867f) 🙂

We now have some coool built-in functions.

[code]

    risp >
    (def a 1)
    // 🔥 => a
    risp >
    (+ a 1)
    // 🔥 => 2
    risp >
    (if (> 2 4 6) 1 2)
    // 🔥 => 2
    risp >
    (if (< 2 4 6) 1 2)
    // 🔥 => 1
[/code]

## Language 2: Full Risp

Now, let’s make this a full-on language. Let’s implement `_lambdas_`! Our
syntax can look like this:

[code]

    (def add-one (fn (a) (+ 1 a)))
    (add-one 1) // => 2
[/code]

### First, create the lambda expression

First things first, let’s introduce a Lambda type for our RispExp

[code]

    #[derive(Clone)]
    enum RispExp {
      Bool(bool),
      Symbol(String),
      Number(f64),
      List(Vec<RispExp>),
      Func(fn(&[RispExp]) -> Result<RispExp, RispErr>),
      Lambda(RispLambda) // bam
    }
    
    #[derive(Clone)]
    struct RispLambda {
      params_exp: Rc<RispExp>,
      body_exp: Rc<RispExp>,
    }
[/code]

Rust will tell us to update `Display` **:**

[code]

     impl fmt::Display for RispExp {
      fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let str = match self {
          ...
          RispExp::Lambda(_) => "Lambda {}".to_string(),
[/code]

Then Rust will tell us to update `eval`:

[code]

    fn eval(exp: &RispExp, env: &mut RispEnv) -> Result<RispExp, RispErr> {
      match exp {
        ...
        RispExp::Lambda(_) => Err(RispErr::Reason("unexpected form".to_string())),
[/code]

### Then, support the built-in constructor

Now, let’s update **eval,** to handle fn — this will be the built-in call that
creates a Lambda expression:

[code]

    fn eval_built_in_form(
      exp: &RispExp, arg_forms: &[RispExp], env: &mut RispEnv
            ...
            "fn" => Some(eval_lambda_args(arg_forms)),
[/code]

`eval_lambda_args` can look like this:

[code]

    fn eval_lambda_args(arg_forms: &[RispExp]) -> Result<RispExp, RispErr> {
      let params_exp = arg_forms.first().ok_or(
        RispErr::Reason(
          "expected args form".to_string(),
        )
      )?;
      let body_exp = arg_forms.get(1).ok_or(
        RispErr::Reason(
          "expected second form".to_string(),
        )
      )?;
      if arg_forms.len() > 2 {
        return Err(
          RispErr::Reason(
            "fn definition can only have two forms ".to_string(),
          )
        )
      }
      
      Ok(
        RispExp::Lambda(
          RispLambda {
            body_exp: Rc::new(body_exp.clone()),
            params_exp: Rc::new(params_exp.clone()),
          }
        )
      )
    }
[/code]

### Then, let’s support scoped environments

For now we only have a global environment. To support lambdas, we need to
introduce the concept of scoped environments. Whenever we call a lambda, we’ll
need to instantiate a new environment.

To do this, let’s first update our `RispEnv` struct, to keep an outer
reference:

[code]

    #[derive(Clone)]
    struct RispEnv<'a> {
      data: HashMap<String, RispExp>,
      outer: Option<&'a RispEnv<'a>>,
    }
[/code]

Let’s update `default_env`, to specify the lifetime and return None as the
outer environment:

[code]

    fn default_env<'a>() -> RispEnv<'a> {
      ... 
      RispEnv {data, outer: None}
    }
[/code]

Then, let’s update `eval`, to recursively search for symbols in our
environment:

[code]

    fn env_get(k: &str, env: &RispEnv) -> Option<RispExp> {
      match env.data.get(k) {
        Some(exp) => Some(exp.clone()),
        None => {
          match &env.outer {
            Some(outer_env) => env_get(k, &outer_env),
            None => None
          }
        }
      }
    }
    
    fn eval(exp: &RispExp, env: &mut RispEnv) -> Result<RispExp, RispErr> {
      match exp {
        RispExp::Symbol(k) =>
          env_get(k, env)
          .ok_or(
            RispErr::Reason(
              format!("unexpected symbol k='{}'", k)
            )
          )
        ,
[/code]

### Finally, let’s support calling lambdas

Let’s update `eval`, so that we know what to do when the first form in a list
is a lambda:

[code]

    fn eval(exp: &RispExp, env: &mut RispEnv) -> Result<RispExp, RispErr> {
              ...
              let first_eval = eval(first_form, env)?;
              match first_eval {
                RispExp::Func(f) => {
                  f(&eval_forms(arg_forms, env)?)
                },
                RispExp::Lambda(lambda) => {
                  let new_env = &mut env_for_lambda(lambda.params_exp, arg_forms, env)?;
                  eval(&lambda.body_exp, new_env)
                },
                _ => Err(
                  RispErr::Reason("first form must be a function".to_string())
                ),
              }
[/code]

We first have a quick helper function to eval a list of expressions, as we’ll
be doing that both for `RispExp::Func` and `RispExp::Lambda`

[code]

    fn eval_forms(arg_forms: &[RispExp], env: &mut RispEnv) -> Result<Vec<RispExp>, RispErr> {
      arg_forms
        .iter()
        .map(|x| eval(x, env))
        .collect()
    }
[/code]

Then, we create a function call `env_for_lambda`. This will get the
`params_exp`, and create an environment, where each param corresponds to the
argument at that index:

[code]

    fn env_for_lambda<'a>(
      params: Rc<RispExp>, 
      arg_forms: &[RispExp],
      outer_env: &'a mut RispEnv,
    ) -> Result<RispEnv<'a>, RispErr> {
      let ks = parse_list_of_symbol_strings(params)?;
      if ks.len() != arg_forms.len() {
        return Err(
          RispErr::Reason(
            format!("expected {} arguments, got {}", ks.len(), arg_forms.len())
          )
        );
      }
      let vs = eval_forms(arg_forms, outer_env)?;
      let mut data: HashMap<String, RispExp> = HashMap::new();
      for (k, v) in ks.iter().zip(vs.iter()) {
        data.insert(k.clone(), v.clone());
      }
      Ok(
        RispEnv {
          data,
          outer: Some(outer_env),
        }
      )
    }
[/code]

To do this, we need the helper `parse_list_of_symbol_strings`, to make sure
all of our param definitions are in fact symbols:

[code]

    fn parse_list_of_symbol_strings(form: Rc<RispExp>) -> Result<Vec<String>, RispErr> {
      let list = match form.as_ref() {
        RispExp::List(s) => Ok(s.clone()),
        _ => Err(RispErr::Reason(
          "expected args form to be a list".to_string(),
        ))
      }?;
      list
        .iter()
        .map(
          |x| {
            match x {
              RispExp::Symbol(s) => Ok(s.clone()),
              _ => Err(RispErr::Reason(
                "expected symbols in the argument list".to_string(),
              ))
            }   
          }
        ).collect()
    }
[/code]

With that, we can `eval(lambda.body_exp, new_env)`, and…

### Voila…language 2.0 is done. [Take a look at the code so
far](https://gist.github.com/stopachka/28b7322eecddf17766e2ee3fa3939cf6) 🙂

We now support lambdas!

[code]

    risp >
    (def add-one (fn (a) (+ 1 a)))
    // 🔥 => add-one
    risp >
    (add-one 1)
    // 🔥 => 2
[/code]

## Fin

And with that, we’ve reached the end of this adventure. I hope it’s been fun!

There’s still a bunch more to implement, and ways we can make this even more
elegant. If you get to it, send me your thoughts 🙂.

Finally, I have to say, I loved using Rust. It’s the least mental overhead
I’ve had to maintain with a systems language, and it was a blast to use. The
community is alive and well, plus — [their guides are
phenomenal](https://doc.rust-lang.org/book)! Give it a shot if you haven’t
already.

* * *

If you liked this post, please share it. For more posts and thoughts, [follow
me on twitter](https://twitter.com/stopachka) 🙂.

* * *

 _Special thanks to Mark Shlick, Taryn Hill, Kaczor Donald, for reviewing this
essay._

 _Thanks to eridius for suggesting a[cleaner
implementation](https://news.ycombinator.com/item?id=19812550) of `parse`
Thanks to thenewwazoo for suggesting a [better
way](https://news.ycombinator.com/item?id=19812159) to do error handling
Thanks to phil_gk for [suggesting the use the
Display](https://www.reddit.com/r/rust/comments/bjy3y9/risp_lisp_in_rust/emeiajb/)
trait_

