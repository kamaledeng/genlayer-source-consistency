# GenLayer Source Consistency Checker

A reusable GenLayer Intelligent Contract for comparing factual information across two external web sources.

## Overview

Source Consistency Checker accepts two source URLs, retrieves their content, and evaluates whether the information presented by both sources is broadly consistent or conflicting.

The contract stores:

- source A
- source B
- verdict
- explanation

## How It Works

1. A user submits two source URLs.
2. The leader retrieves both sources using GenLayer web access.
3. The leader evaluates the information from both sources.
4. Validators independently retrieve and evaluate the same sources.
5. The validator compares its verdict with the leader decision.
6. GenLayer consensus determines whether the transaction is accepted.
7. The final result is stored in contract state.

## Consensus

The contract uses GenLayer's non-deterministic execution because external web content and language-model evaluation are not deterministic blockchain operations.

The validator checks that the leader and validator reach the same classification:

- `consistent`
- `conflicting`

## Example

Source A:

`https://genlayer.com/`

Source B:

`https://genlayer.com/`

Result:

`consistent`

The comparison was executed through Full Consensus in GenLayer Studio.

## Use Cases

This primitive can be extended for:

- research source comparison
- evidence verification
- source consistency checking
- automated research workflows
- decentralized information verification

## Contract State

```text
source_a
source_b
verdict
explanation
