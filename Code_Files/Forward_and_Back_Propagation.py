#!/usr/bin/env python
# coding: utf-8

# # Understanding Forward and Back Propagation =============

# In[169]:


import math


# In[170]:


import math

def f(x1, x2):
    try:
        return x1 * math.exp(x2) + math.cos(x1 * x2)
    except OverflowError as e:
        print(f'x1:{x1}, x2:{x2}')
        raise RuntimeError("Overflow in f(x1,x2)") from e


# In[171]:


import math

def compute_deltas(x1, x2, lr = 1e-3, prnt = True, prnt_delta = True):
    # ----- forward pass -----
    v1 = x1
    v2 = x2
    v3 = math.exp(v2)
    v4 = v1 * v3
    v5 = v1 * v2
    v6 = math.cos(v5)
    v7 = v4 + v6
    f_old = v7

    if prnt:
        print(f"v1 = {v1}")
        print(f"v2 = {v2}")
        print(f"v3 = {v3}")
        print(f"v4 = {v4}")
        print(f"v5 = {v5}")
        print(f"v6 = {v6}")
        print(f"v7 = {v7}")

    # ----- backward pass -----
    dv7 = 1.0

    dv4 = dv7 * 1.0
    dv6 = dv7 * 1.0

    dv5 = dv6 * (-math.sin(v5))

    dv1_from_v4 = dv4 * v3
    dv3 = dv4 * v1

    dv1_from_v5 = dv5 * v2
    dv2_from_v5 = dv5 * v1

    dv2_from_v3 = dv3 * math.exp(v2)

    dv1 = dv1_from_v4 + dv1_from_v5
    dv2 = dv2_from_v5 + dv2_from_v3

    # ----- print deltas -----
    if prnt:
        print(f"dv7 = {dv7}")
        print(f"dv6 = {dv6}")
        print(f"dv5 = {dv5}")
        print(f"dv4 = {dv4}")
        print(f"dv3 = {dv3}")
        print(f"dv2 = {dv2}")
        print(f"dv1 = {dv1}")


    # Optimizer
    # ----- update -----
    x1_new = x1 - lr * dv1
    x2_new = x2 - lr * dv2
    f_new = f(x1_new, x2_new)

    if prnt:
        print(f"x1_new = {x1_new}")
        print(f"x2_new = {x2_new}")

    if prnt_delta:
        delta_f = f_new - f_old
        if delta_f>0:
            print(f"delta_f = {delta_f}  (should be < 0 for descent)")
        else:
            print(f"delta_f = {delta_f}")
        print(f"f_new={f_new}, f_old={f_old}")
        print('-'*25)


    return x1_new,x2_new


# In[172]:


x1,x2 = 0.6,0.6
for i in range(2):
    x1,x2 = compute_deltas(x1,x2,1e-2, prnt = False, prnt_delta = True)


# In[173]:


print(f'x1:{x1}, x2:{x2}')


# In[174]:


x1,x2 = 0.5,0.5
for i in range(1):
    print(f'Step : {i+1}')
    x1,x2 = compute_deltas(x1,x2,1e-4, prnt = True, prnt_delta = False)
    print('='*25)


# In[175]:


print(f'x1:{x1}, x2:{x2}')


# In[ ]:





# # Forward backward with loss

# In[176]:


import math

def compute_deltas_make_v7_zero(x1, x2, v_target=0, lr=1e-3, prnt=False, prnt_delta=True):
    # ----- forward pass -----
    v1 = x1
    v2 = x2
    v3 = math.exp(v2)
    v4 = v1 * v3
    v5 = v1 * v2
    v6 = math.cos(v5)
    v7 = v4 + v6

    # loss: 1/2 * (v7 - v_target)^2
    L_old = 0.5 * (v7 - v_target) ** 2

    # ----- backward pass -----
    # dv_k := ∂L/∂v_k  (gradient of total loss w.r.t. v_k)
    # dL/dv7 = v7 - v_target
    dv7 = v7 - v_target  # Main change (loss decides this)

    dv4 = dv7
    dv6 = dv7

    dv5 = dv6 * (-math.sin(v5))

    dv1_from_v4 = dv4 * v3
    dv3 = dv4 * v1

    dv1_from_v5 = dv5 * v2
    dv2_from_v5 = dv5 * v1

    dv2_from_v3 = dv3 * v3  # exp(v2)

    dv1 = dv1_from_v4 + dv1_from_v5
    dv2 = dv2_from_v5 + dv2_from_v3

    # ----- update -----
    x1_new = x1 - lr * dv1
    x2_new = x2 - lr * dv2

    # new loss
    v7_new = x1_new * math.exp(x2_new) + math.cos(x1_new * x2_new)
    L_new = 0.5 * (v7_new - v_target) ** 2

    if prnt_delta:
        print(f"v7_old={v7:.6f}, v7_new={v7_new:.6f}")
        print(f"L_old={L_old:.6f}, L_new={L_new:.6f}, delta_L={L_new - L_old:.6f}")
        print("-" * 25)

    return x1_new, x2_new


# In[177]:


x1,x2 = 0.5,0.5
for i in range(5000):
    #print(f'Step : {i+1}')
    x1,x2 = compute_deltas_make_v7_zero(x1,x2,lr = 1e-3, prnt = False, prnt_delta = False)
    #print('='*25)
print(f'x1:{x1}, x2:{x2}')


# In[178]:


x1,x2 = 1.5,1.5
for i in range(5000):
    #print(f'Step : {i+1}')
    x1,x2 = compute_deltas_make_v7_zero(x1,x2,v_target = 0, lr = 1e-3, prnt = False, prnt_delta = False)
    #print('='*25)
print(f'x1:{x1}, x2:{x2}')


# In[179]:


x1,x2 = 1.5,1.5
for i in range(5000):
    #print(f'Step : {i+1}')
    x1,x2 = compute_deltas_make_v7_zero(x1,x2,v_target = 1, lr = 1e-3, prnt = False, prnt_delta = False)
    #print('='*25)
print(f'x1:{x1}, x2:{x2}')
print(f(x1,x2))


# In[180]:


x1,x2 = 2,5
for i in range(5000):
    #print(f'Step : {i+1}')
    x1,x2 = compute_deltas_make_v7_zero(x1,x2,v_target = 1, lr = 1e-3, prnt = False, prnt_delta = False)
    #print('='*25)
print(f'x1:{x1}, x2:{x2}')
print(f(x1,x2))


# In[ ]:





# # Canonical NN structure ===============================

# In[194]:


import math
import numpy as np

def relu(z):
    return np.maximum(0.0, z)

def relu_grad(z):
    return (z > 0).astype(float)

def softmax(z):
    z = z - np.max(z)        # numerical stability
    expz = np.exp(z)
    return expz / np.sum(expz)


# In[195]:


def forward(x, params):
    W1, b1, W2, b2, W3, b3, W4, b4 = params

    # Layer 1
    z1 = W1 @ x + b1
    a1 = relu(z1)

    # Layer 2
    z2 = W2 @ a1 + b2
    a2 = relu(z2)

    # Layer 3
    z3 = W3 @ a2 + b3
    a3 = relu(z3)

    # Output layer
    z4 = W4 @ a3 + b4
    y_hat = softmax(z4)

    cache = (x, z1, a1, z2, a2, z3, a3, z4, y_hat)
    return y_hat, cache


# In[196]:


def backward(y, cache, params):
    W1, b1, W2, b2, W3, b3, W4, b4 = params
    x, z1, a1, z2, a2, z3, a3, z4, y_hat = cache

    # ----- output layer delta -----
    dz4 = y_hat - y                 # dv7 equivalent (vector)

    dW4 = np.outer(dz4, a3)
    db4 = dz4

    #---------
    da3 = W4.T @ dz4
    dz3 = da3 * relu_grad(z3)

    dW3 = np.outer(dz3, a2)
    db3 = dz3

    #---------
    da2 = W3.T @ dz3
    dz2 = da2 * relu_grad(z2)

    dW2 = np.outer(dz2, a1)
    db2 = dz2

    #---------
    da1 = W2.T @ dz2
    dz1 = da1 * relu_grad(z1)

    dW1 = np.outer(dz1, x)
    db1 = dz1

    grads = (dW1, db1, dW2, db2, dW3, db3, dW4, db4)
    return grads


# In[197]:


def step(params, grads, lr):
    return tuple(p - lr * g for p, g in zip(params, grads))


# ## Example

# ### Init Params

# In[198]:


np.random.seed(0)

W1 = 0.1 * np.random.randn(4, 2)
b1 = np.zeros(4)

W2 = 0.1 * np.random.randn(4, 4)
b2 = np.zeros(4)

W3 = 0.1 * np.random.randn(3, 4)
b3 = np.zeros(3)

W4 = 0.1 * np.random.randn(2, 3)
b4 = np.zeros(2)

params = (W1, b1, W2, b2, W3, b3, W4, b4)


# ### Init In/out

# In[199]:


x = np.array([0.5, -1.0])   # input
y = np.array([1.0, 0.0])    # target (one-hot)
print(f'\nx:{x}, \ny:{y}')


# ### Forward Pass

# In[200]:


y_hat, cache = forward(x, params)

print("Prediction:", y_hat)
print("Sum:", y_hat.sum())  # should be 1 (softmax)


# ### Compute loss

# In[201]:


loss = -np.sum(y * np.log(y_hat + 1e-12))
print("Loss:", loss)


# ### Backward pass

# In[202]:


grads = backward(y, cache, params)
grads_name = ['dW1', 'db1', 'dW2', 'db2', 'dW3', 'db3']
for name, val in zip(grads_name,grads):
    print(f'{name}:\n{val} ')
    print('='*25)


# ### Gradient descent update

# In[203]:


lr = 1e-2
params = step(params, grads, lr)
params_name = ['W1+', 'b1+', 'W2+', 'b2+', 'W3+', 'b3+']
for name, val in zip(params_name,params):
    print(f'{name}:\n{val} ')
    print('='*25)


# ### Full training loop (minimal)

# In[204]:


for step_id in range(10001):
    y_hat, cache = forward(x, params)
    loss = -np.sum(y * np.log(y_hat + 1e-12))
    grads = backward(y, cache, params)
    params = step(params, grads, lr=1e-2)

    if step_id % 2000 == 0:
        print(f"step {step_id}, loss = {loss:.6f}")


# In[ ]:





# In[ ]:





# In[ ]:




