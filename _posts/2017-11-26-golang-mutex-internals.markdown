---
layout: post
title:  "Mutex and RWMutex in Go"
date:   2017-11-26 20:46:40 +0500
categories: golang
---
# Mutexes in Go

## Intro

Mutexes are used to protect memory area from mutation by multiple goroutines at the same time.
Memory protection is done to avoid side-effects in the program. In other cases this can bring to
unknown behaviour in runtime and Go memory model does not guarantee correct work if you are corrupting the memory.
Go runtime has a race detector, it can be enable by passing `-race` flag to the compiler:

```Golang
go build -race
go test . -race
```

[Read more about the race detector](https://golang.org/doc/articles/race_detector.html)

The `sync` package provides two types of mutexes:

* `Mutex`
* `RWmutex`

The difference between them will be explained in this blog post.

## Mutex

The `sync.Mutex` structure implements `sync.Locker` interface and has two methods:

* `Lock()`
* `Unlock()`

`Lock()` locks the memory and if other goroutine tries to call Lock() method, the goroutines will be blocked
until the Unlock() method will not be called and makes the lock available for other goroutines.
You must hold the lock while you're mutating memory.
For example:

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
And there can be a moment when one goroutine gets state and another one mutates the map **at the same time**
and this will be a data race that bring to the memory corruption.
To avoid this, these operations must be done atomically or consequently.
There we start protecting memory with mutex and our initial verssion of code will change:

```Golang
var m = map[string]int{}
var lock = new(sync.Mutex)

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

This fixes the code and there will not be data races.
The map state is read and written atomically.
If the goroutine #1 is reading the state it acquires the lock.
and if the goroutine #2 want to change/read the state at the same time,
it has to wait until the lock will not be released by the gorotuines #1.
That's nice and we are satisfied with it.

But, what if we change the state once in hour and read every second.
Reading the state concurrently does mutate the shared state and it is race free.
The idea is to let allow multiple goroutines to hold the lock for reading,
but only one goroutine can hold the lock for writing. There comes a `RWMutex`

## RWMutex

`RWMutex` or read write mutex allows multiple goroutines to hold the read lock but only one goroutines can hold the write lock:

>A RWMutex is a reader/writer mutual exclusion lock. The lock can be held by an arbitrary number of readers or a single writer. The zero value for a RWMutex is an unlocked mutex.

`RWMutex` has adds couple more methods to acquire and release the lock only for reading:

* `RLock()` acquires the lock for reading, and it can be held my multiple goroutines.
* `RUnlock()` releases the single RLock().

`Lock()` locks the state for writing, and if the lock is held by gorotuines for reading,
it waits until the read lock is realeased and does not let other goroutines to acquire the lock:

>Lock locks rw for writing. If the lock is already locked for reading or writing, Lock blocks until the lock is available.
>If a goroutine holds a RWMutex for reading and another goroutine might call Lock, no goroutine should expect to be able to acquire a read lock until the initial read lock is released. In particular, this prohibits recursive read locking. This is to ensure that the lock eventually becomes available; a blocked Lock call excludes new readers from acquiring the lock.

The second version of code that used Mutex will be changed:

```Golang
var m = map[string]int{}
var lock = new(sync.RWMutex)

func mutate(key string, val int) {
    l.Lock()
    m[k] = v
    l.Unlock()

    return
}

func state(key string) (int, bool) {
    l.RLock()
    val, ok := m[key]
    l.RUnlock()

    return val, ok
}
```

We just simply replaced `Mutex` with `RWMutex`, and calling `RLock`, `RUnlock` instead of `Lock` and `Unlock` while reading the state.

[Read here to know about Mutex internals in Golang](https://medium.com/golangspec/sync-rwmutex-ca6c6c3208a0)

## References

* [Go sync package documentation](https://godoc.org/sync)
* [Go maps in action blog post](https://blog.golang.org/go-maps-in-action#TOC_6.)