# Value of constants
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
G = (55066263022277343669578718895168534326250603453777594175500187360389116729240,32670510020758816978083085130507043184471273380659243275938904335757337482424)
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337

def inverse(a, m):
    m_orig = m
    if(a < 0):
      a = a%m
    prevy, y = 0, 1
    while(a > 1):
       q = m//a
       y, prevy = prevy-q*y, y
       a, m = m%a, a
    return y%m_orig

def double(point):
  # slope = (3x₁² + a) / 2y₁
  slope = (((3 * (point[0] ** 2)) * inverse((2 * point[1]), p))) % p # using inverse to help with division

  # x = slope² - 2x₁
  x = (slope ** 2 - (2 * point[0])) % p

  # y = slope * (x₁ - x) - y₁
  y = (slope * (point[0] - x) - point[1]) % p

  # Return the new point
  return (x, y)

def add(point1, point2):
  # double if both points are the same
  if (point1 == point2):
    return double(point1)

  # slope = (y₁ - y₂) / (x₁ - x₂)
  slope = ((point1[1] - point2[1]) * inverse(point1[0] - point2[0], p)) % p

  # x = slope² - x₁ - x₂
  x = (slope ** 2 - point1[0] - point2[0]) % p

  # y = slope * (x₁ - x) - y₁
  y = ((slope * (point1[0] - x)) - point1[1]) % p

  # Return the new point
  return (x, y)

def multiply(k, point):
  # create a copy the initial starting point (for use in addition later on)
  current = point

  # convert integer to binary representation
  binary = bin(k)[2:]

  # double and add algorithm for fast multiplication
  for char in binary[1:]:
    current = double(current)

    # 1 = double and add
    if (char == "1"):
       current = add(current, point) 

  # return the final point
  return current

def verify(pkt, st, hash):
    point1 = multiply(inverse(st[1], n) * hash, G)
    point2 = multiply((inverse(st[1], n) * st[0]), pkt)
    point3 = add(point1, point2)
    return point3[0] == st[0]

def decodesig(sig):
    r = ""
    rl = int(sig[6:8], 16)
    for i in range(8, 8+rl*2):
      r += sig[i]
    s = ""
    sl = int(sig[8+rl*2+2 : 8+rl*2+4], 16)
    for i in range(8+rl*2+4, 8+rl*2+4+sl*2):
      s += sig[i]
    ri = int(r, 16)
    si = int(s, 16)
    return (ri, si)

def decodepk(pk):
    prefix = pk[0:2]
    x = int(pk[2:], 16)
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    y_sq = (pow(x, 3, p) + 7) % p
    y = pow(y_sq, (p+1)//4, p)
    if y % 2 != int(prefix) % 2:
        y = p - y
    return (x, y)

