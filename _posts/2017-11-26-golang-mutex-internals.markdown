---
layout: post
title:  "Golang mutex internals"
date:   2017-11-26 20:46:40 +0500
categories: golang
---
# Mutexes in Go

## Intro
Mutexes are used to protect memory area from mutation by multiple goroutines at the same time.
Memory protection is done to avoid side-effects in the program. In other case this can bring to
unknown behaviour in runtime and Go memory model does not guarantee correct work if you are corrupting the memory.
But there is a very handy tool in Golang toolbox that helps to detect data races in Go code. It helps
to find data races while running tests and while running the programming. This is done by 
setting `-race` flag on running tests and compiling. More about this: https://golang.org/doc/articles/race_detector.html

Golang has two types of mutexes `Mutex` and `RWmutex` in `sync` package. The difference will be explained.
This blog post covers types of mutexes in and detailed information about their implemenatation.

## Mutex and RWMutex
The sync package has two types of mutexes: Mutex and RWMutex.

The sync.Mutex structure implements sync.Locker interface and has two methods: Lock() and Unlock()
Lock() - locks the memory and if other goroutine tries to call Lock() method, this action will be blocked
until the Unlock() method will not be called and makes the lock available for other goroutines. You must hold the
lock while you're mutating memory. For example some value of map. Here is a code snippet that shows why it is needed:
```Golang
var m = map[string]int{}

func mutate(key string, val int) {
    m[k] = v

    return
}

func state(key string) (int, bool) {
    val, ok := [key]
    return val, ok
}
```

Let's suppose that we have dozens of goroutines that try to call mutate and state functions concurrently.
And there can be a moment when one goroutine gets state and another one mutates the map at the same time.
In this case, there can be a data race and bring to the undefined behaviour and corrupt the memory.
To avoid this we must do these operations atomically or consequently. There we start protecting memory with mutex.
Code changes:

```Golang
var m = map[string]int{}
+ var lock = new(sync.Mutex)

func mutate(key string, val int) {
    l.Lock()
    m[k] = v
    l.Unlock()

    return
}

func state(key string) (int, bool) {
    l.Lock()
    val, ok := m[key]
    l.Unlock()

    return val, ok
}
```

This fixes the code, and there are no data races anymore. But, why we must lock the memory if we want just read data from it.
Multiple goroutines can read data from map concurrently and this will not bring to data race and we are not obligated to do
this process atomically.

That is why we have RWMutex! We can read data concurrently and lock the memoy when there are mutations.
## Mutex internals

## RWMutex internals

## References