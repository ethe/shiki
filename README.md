# shiki (式)
==========================

[![Build Status](https://travis-ci.org/ethe/shiki.svg?branch=master)](https://travis-ci.org/ethe/shiki) [![codecov.io](https://codecov.io/gh/ethe/shiki/badge.svg)](https://codecov.io/gh/ethe/shiki)

A toy language, slow, simple and useless.

一门简单的、为了学习如何写语言而写的语言。


## Binding
```
let foo = 1
```

## Function and call
```
let a = 1

func foo n do
  return + a n
end

foo 2
```

## Tail call optimization
```
func foo do
  return bar
end

func bar do
  return foo
end

foo
```
