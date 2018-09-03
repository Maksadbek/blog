---
layout: home
title:  "Mutex and RWMutex in Go"
date:   2017-11-26 20:46:40 +0500
categories: golang
---

# Mutex and RWMutex in Go

Go has builtin facilities for writing concurrent programs.
The concurrency pattern is implemented with CSP(Communication Sequential Processes) model that was introduced by Tony Hoare in 1978.
The concurrent code in Go is written using goroutines and channels.
Goroutines are functions that run simultaneously and usually use channels to synchronize with each other.
To run a function as a goroutine, it must be invocated with `go` keyword: `go listen()`

Goroutines can have a common shared state and communication to access that state can be done via channels or via just accessing that shared state.
The popular Go proverb is:
> Don't communicate by sharing memory, share memory by communicating. (Rob Pike)

That is, communication is done better and clearer when you share the state via channels through goroutines than directly accessing the shared state.

This blog post does cover the channel communication.
It explains how to safely access the shared state using mutual exclusions in Go.

Mutexes are used to protect the shared state from mutation by multiple goroutines at the same time.
The protection is needed to avoid the undefined behavior of the program.
Go memory model does not guarantee the correct work if there are data races.
That is, one goroutine writes to a shared variable neither before nor after another goroutine's write/read happened. They are doing it simultaneously.
Fortunately, Go runtime has a race detector, it is enabled with passing `-race` flag to the compiler:

```Golang
go build -race
go test . -race
```

[Read more about race detector](https://golang.org/doc/articles/race_detector.html)

The `sync` package implements two types of mutexes:

* `Mutex`
* `RWmutex`

## Mutex

The `sync.Mutex` implements `sync.Locker` interface and has two methods:

* `Lock()`
* `Unlock()`

`Lock()` acquires the lock and if another goroutine will call `Lock()` -- it will be blocked
until the `Unlock()` will not release the lock and makes it available for other goroutines.
So, the lock must be held while the shared state is being mutated.
For example we a map and two functions, one mutates it, another one reads from it:

```Golang
package main

var m = map[string]int{}

func mutate(key string, val int) {
    m[k] = v
    return
}

func state(key string) (int, bool) {
    val, ok := m[key]
    return val, ok
}

func main() {
    mutate("foo", 1)
    v, ok := state("foo")
    println(v, ok)
}
```

It is ok since reading/writing to the map is not happening at the same time. There is no concurrency in the code.
Go memory model guarantees the order of execution of instructions that are written in the code:
state starts after mutating returns.

But if we want to execute `mutate` concurrently, with a `go` keyword, race detector will warn about the possible data race.
Multiple goroutines must synchronize and change the shared variable atomically to establish [happens-before conditions](https://golang.org/ref/mem#tmp_2).

We have two goroutines that execute mutate and state functions concurrently.
There can be a momentum when one goroutine reads state and another one changes it **at the same time**
and this will be a data race that will bring to the memory corruption.
To avoid this, goroutines must use synchronization primitives while accessing the shared stated.
In other words, concurrent operations must be done atomically(consequently) but not at same time.
There we start protecting memory with the mutex and our initial version of the code has changed:

```Golang
package main

import (
    "sync"
)

var m = map[string]int{}
var mutex = new(sync.Mutex)

func mutate(key string, val int) {
    mutex.Lock()
    m[key] = val
    mutex.Unlock()

    return
}

func state(key string) (int, bool) {
    var val int
    var ok bool

    mutex.Lock()
    val, ok = m[key]
    mutex.Unlock()

    return val, ok
}

func main() {
        go mutate("foo", i)
        val, ok := state("foo", i)
        println(val, ok)
}
```

This makes concurrent read/write operations safely and there will not be data races.
The map's state is read and written atomically.
If the goroutine #1 is reading the state it acquires the lock.
Then, when goroutine #2 want to change/read the state at the same time,
it has to wait until the lock will not be released by the goroutines #1.
That's ok for now and we are satisfied with that.

But, what if we change the state once in an hour and read every second.
Reading the state concurrently does mutate the shared state and it is race free.
The idea is to let multiple goroutines to hold the lock for reading,
but only one goroutine can hold the lock for writing.
There comes a `RWMutex`!

## RWMutex

`RWMutex` or read-write mutex allows multiple goroutines to hold the read lock but only one goroutine can hold the write lock:

>A RWMutex is a reader/writer mutual exclusion lock. The lock can be held by an arbitrary number of readers or a single writer. The zero value for an RWMutex is an unlocked mutex.

`RWMutex` has added a couple more methods to acquire and release the lock only for reading:

* `RLock()` acquires the lock for reading, and it can be held by multiple goroutines.
* `RUnlock()` releases the single RLock().

`Lock()` locks the state for writing, and if the lock is held by goroutines for reading,
it waits until the read lock is released and does not let other goroutines to acquire the lock:

>Lock locks rw for writing. If the lock is already locked for reading or writing, Lock blocks until the lock is available.
>If a goroutine holds a RWMutex for reading and another goroutine might call Lock, no goroutine should expect to be able to acquire a read lock until the initial read lock is released. In particular, this prohibits recursive read locking. This is to ensure that the lock eventually becomes available; a blocked Lock call excludes new readers from acquiring the lock.

The second version of the code that used Mutex will be changed:

```Golang
package main

import (
    "sync"
    "time"
)

var m = map[string]int{}
var mutex = new(sync.RWMutex)

func mutate(key string, val int) {
    mutex.Lock()
    m[key] = val
    mutex.Unlock()

    return
}

func state(key string) (int, bool) {
    mutex.RLock()
    val, ok := m[key]
    mutex.RUnlock()

    return val, ok
}

func main() {
    readTicker := time.NewTicker(100 * time.Millisecond)

    go func() {
        for _ = range readTicker.C {
            state("foo")
        }
    }()

    writeTicker := time.NewTicker(500 * time.Millisecond)
    go func() {
        for _ = range writeTicker.C {
            mutate("foo", 1)
        }
    }()

    time.Sleep(1600 * time.Millisecond)
    writeTicker.Stop()
    readTicker.Stop()
}
```

We just simply replaced `Mutex` with `RWMutex`, and calling `RLock`, `RUnlock` instead of `Lock` and `Unlock` while reading the state.

[Read here to know about Mutex internals in Golang](https://medium.com/golangspec/sync-rwmutex-ca6c6c3208a0)

## References

* [Go sync package documentation](https://godoc.org/sync)
* [Go maps in action blog post](https://blog.golang.org/go-maps-in-action#TOC_6.)