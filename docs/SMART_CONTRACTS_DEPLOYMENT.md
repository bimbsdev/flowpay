# Smart Contracts - Testing & Deployment Guide

## Overview

FlowPay includes 4 production-grade Soroban smart contracts written in Rust (1,615 lines):

1. **Payment Channel** - Low-cost micropayment settlement
2. **Escrow** - Conditional fund release with multi-party approval
3. **Merchant Registry** - On-chain merchant identity management
4. **Recurring Payment** - Subscription-based recurring payments

---

## Prerequisites

### 1. Install Soroban CLI

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

# Install Soroban CLI
cargo install soroban-cli

# Verify installation
soroban --version  # Should show v21.0.0 or higher
```

### 2. Setup Stellar Account

```bash
# Create testnet account
soroban keys generate flowpay --network testnet

# Get account address
soroban keys address flowpay

# Fund account (visit https://laboratory.stellar.org/#account-creator?network=testnet)
# Or use: soroban keys fund flowpay --network testnet
```

---

## Contract Structure

```
contracts/
├── Cargo.toml              # Rust dependencies
├── src/
│   ├── lib.rs             # Contract entry point
│   ├── payment_channel.rs  # Payment channel contract
│   ├── escrow.rs          # Escrow contract
│   ├── merchant_registry.rs # Merchant registry contract
│   └── recurring_payment.rs # Recurring payment contract
└── tests/
    └── integration_tests.rs # Integration tests (if present)
```

---

## Building Contracts

### 1. Build All Contracts

```bash
cd contracts

# Build in debug mode
soroban contract build

# Or build with optimizations
cargo build --target wasm32-unknown-unknown --release
```

### 2. Build Individual Contracts

```bash
# Payment Channel
rustc --target wasm32-unknown-unknown -C opt-level=z \
  --edition 2021 src/payment_channel.rs -o payment_channel.wasm

# Escrow
rustc --target wasm32-unknown-unknown -C opt-level=z \
  --edition 2021 src/escrow.rs -o escrow.wasm
```

### 3. Verify Build Artifacts

```bash
# Check contract sizes
ls -lh *.wasm

# Optimal size: < 100KB
# Payment Channel: ~45KB
# Escrow: ~50KB
# Merchant Registry: ~48KB
# Recurring Payment: ~47KB
```

---

## Contract Deployment

### 1. Deploy Payment Channel Contract

```bash
# Set network
export NETWORK=testnet
export RPC_URL=https://soroban-testnet.stellar.org
export ACCOUNT=flowpay

# Build contract
soroban contract build

# Deploy contract
soroban contract deploy \
  --wasm target/wasm32-unknown-unknown/release/flowpay.wasm \
  --source $ACCOUNT \
  --network $NETWORK

# Output: CABC1234567890ABCDEF... (save this!)
export PAYMENT_CHANNEL_ID=<contract_address>
```

### 2. Deploy Escrow Contract

```bash
soroban contract deploy \
  --wasm target/wasm32-unknown-unknown/release/escrow.wasm \
  --source $ACCOUNT \
  --network $NETWORK

export ESCROW_ID=<contract_address>
```

### 3. Deploy Merchant Registry Contract

```bash
soroban contract deploy \
  --wasm target/wasm32-unknown-unknown/release/merchant_registry.wasm \
  --source $ACCOUNT \
  --network $NETWORK

export MERCHANT_REGISTRY_ID=<contract_address>
```

### 4. Deploy Recurring Payment Contract

```bash
soroban contract deploy \
  --wasm target/wasm32-unknown-unknown/release/recurring_payment.wasm \
  --source $ACCOUNT \
  --network $NETWORK

export RECURRING_PAYMENT_ID=<contract_address>
```

### 5. Update Environment Variables

```bash
# backend/.env
PAYMENT_CHANNEL_CONTRACT_ID=$PAYMENT_CHANNEL_ID
ESCROW_CONTRACT_ID=$ESCROW_ID
MERCHANT_REGISTRY_CONTRACT_ID=$MERCHANT_REGISTRY_ID
RECURRING_PAYMENT_CONTRACT_ID=$RECURRING_PAYMENT_ID
```

---

## Testing Contracts

### 1. Unit Tests

```bash
cd contracts

# Run tests (if test files exist)
cargo test

# Run specific test
cargo test payment_channel::tests
```

### 2. Integration Testing

```bash
# Invoke contract methods directly
soroban contract invoke \
  --id $PAYMENT_CHANNEL_ID \
  --source $ACCOUNT \
  --network $NETWORK \
  -- initialize_channel \
  --payer $(soroban keys address $ACCOUNT) \
  --recipient GXXXXXXXXX... \
  --asset $(soroban keys address $ACCOUNT) \
  --amount 1000000
```

### 3. Query Contract State

```bash
# Read contract state
soroban contract read \
  --id $PAYMENT_CHANNEL_ID \
  --key "Channel($(soroban keys address $ACCOUNT))" \
  --network $NETWORK
```

### 4. Monitor Contract Events

```bash
# Stream contract events
soroban events watch \
  --id $PAYMENT_CHANNEL_ID \
  --network $NETWORK
```

---

## Contract Verification

### 1. Verify on Stellar Expert

Visit: https://expert.stellar.org/

1. Enter contract ID
2. View source code (if verified)
3. Check transaction history
4. Inspect contract data

### 2. Verify Locally

```bash
# Get contract details
soroban contract info \
  --id $PAYMENT_CHANNEL_ID \
  --network $NETWORK

# Get contract metadata
soroban contract meta \
  --id $PAYMENT_CHANNEL_ID \
  --network $NETWORK
```

---

## Troubleshooting

### Build Issues

```bash
# Clear build cache
cargo clean

# Update dependencies
cargo update

# Check Rust version
rustc --version  # Should be 1.70+
```

### Deployment Issues

```bash
# Check account balance
soroban account balance $ACCOUNT --network testnet

# Check RPC endpoint
curl -X POST https://soroban-testnet.stellar.org \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"getNetwork","params":[]}'

# Check contract status
soroban contract info --id $PAYMENT_CHANNEL_ID --network testnet
```

---

## Contract Specifications

### Payment Channel Contract

**Methods:**
- `initialize_channel(payer, recipient, asset, amount)` - Create channel
- `authorize_payment(payer, amount, nonce)` - Authorize payment
- `claim(payer, amount)` - Claim payment
- `refund(payer)` - Refund balance
- `close(payer)` - Close channel

**Events:**
- `ChannelCreated` - Channel opened
- `PaymentAuthorized` - Payment authorized
- `PaymentClaimed` - Payment claimed
- `ChannelClosed` - Channel closed

### Escrow Contract

**Methods:**
- `create_escrow(payer, payee, arbitrator, asset, amount, release_at, expires_at)` - Create escrow
- `approve(escrow_id)` - Approve release
- `release(escrow_id)` - Release funds
- `cancel(escrow_id)` - Cancel escrow

**Events:**
- `EscrowCreated`
- `EscrowApproved`
- `EscrowReleased`
- `EscrowCancelled`

### Merchant Registry Contract

**Methods:**
- `initialize(admin)` - Initialize with admin
- `register(merchant_id, wallet_address, name, fee_percent)` - Register merchant
- `set_fee(merchant_id, new_fee_percent)` - Update fee
- `set_status(merchant_id, status)` - Update status

**Events:**
- `MerchantRegistered`
- `MerchantUpdated`
- `FeeUpdated`
- `StatusChanged`

### Recurring Payment Contract

**Methods:**
- `create_subscription(subscriber, merchant, asset, amount, frequency, duration)` - Create subscription
- `execute_cycle(subscription_id)` - Execute payment cycle
- `pause(subscription_id)` - Pause subscription
- `resume(subscription_id)` - Resume subscription

**Events:**
- `SubscriptionCreated`
- `PaymentExecuted`
- `SubscriptionPaused`
- `SubscriptionResumed`

---

## Production Checklist

- [ ] All contracts deployed to testnet
- [ ] Contract IDs added to `.env`
- [ ] Integration tests passing
- [ ] Contract methods verified on Stellar Expert
- [ ] Events being emitted correctly
- [ ] Rate limiting prevents abuse
- [ ] Error handling for failed transactions
- [ ] Documentation complete
- [ ] Contracts ready for mainnet deployment

---

## Security Considerations

1. **Replay Protection** - All contracts use nonce-based replay prevention
2. **Authorization Checks** - All sensitive operations require caller authentication
3. **Time Locks** - Escrow implements time-locked fund release
4. **Status Management** - Merchant registry enforces proper state transitions
5. **Event Logging** - All state changes emit events for auditability

---

## Further Reading

- [Soroban Documentation](https://developers.stellar.org/learn/build/smart-contracts)
- [Stellar CLI Reference](https://github.com/stellar/rs-soroban-sdk)
- [Contract Examples](https://github.com/stellar/rs-soroban-sdk/tree/master/examples)

