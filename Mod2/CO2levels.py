import numpy as np
import matplotlib.pyplot as plt

N = 40
m = 1.0
beta = 1.0
trajectories = {}
linear_cases = [
    ("(a) alpha=0.2", 0.2),
    ("(b) alpha=0.5", 0.5),
    ("(c) alpha=1.0", 1.0),
    ("(d) alpha=1.2", 1.2),
]
nl_cases = [
    ("(a) k=0.1", 0.1),
    ("(b) k=0.5", 0.5),
    ("(c) k=1.0", 1.0),
    ("(d) k=1.5", 1.5),
]


# linear model helpers
def iterate_linear(alpha, beta, m, C0, C1, N):
    """C_{n+1} = C_n - alpha*beta*C_{n-1} + m   (5)"""
    C = np.zeros(N + 1)
    C[0], C[1] = C0, C1
    for n in range(1, N):
        C[n + 1] = C[n] - alpha * beta * C[n - 1] + m
    return C


def closed_form_complex(alpha, beta, m, C0, C1, N):
    """Valid for 4*alpha*beta > 1"""
    p = alpha * beta
    Cs = m / p
    r = np.sqrt(p)
    theta = np.arccos(1 / (2 * r))
    A = C0 - Cs
    B = ((C1 - Cs) / r - A * np.cos(theta)) / np.sin(theta)
    n = np.arange(N + 1)
    return Cs + r**n * (A * np.cos(theta * n) + B * np.sin(theta * n))

# nonlinear model helpers
def iterate_nonlinear(alpha, beta, m, C0, V0, N, blowup=50.0):
    """C_{n+1} = C_n - beta*V_n*C_n + m ;  V_{n+1} = alpha*C_n (5, 6)"""
    C = np.full(N + 1, np.nan)  # NaN -> not plotted
    V = np.full(N + 1, np.nan)
    C[0], V[0] = C0, V0
    for n in range(N):
        C[n + 1] = C[n] - beta * V[n] * C[n] + m
        V[n + 1] = alpha * C[n]
        if abs(C[n + 1]) > blowup:
            break
    return C, V

def steady_state(alpha, beta, m):
    return np.sqrt(m / (alpha * beta)), np.sqrt(alpha * m / beta)


def fig1(plot):
    fig = plot[0]
    for ax, (title, alpha) in zip(plot[1].flat, linear_cases):
        C = iterate_linear(alpha, beta, m, 2.0, 2.0, N)
        Cs = m / (alpha * beta)
        ax.plot(range(N + 1), C, "o-", ms=4, label="iterated $C_n$")
        ax.axhline(Cs, ls="--", color="gray", label=f"$C^*$ = {Cs:.2f}")
        if alpha == 0.5: 
            ax.plot(range(N + 1), closed_form_complex(alpha, beta, m, 2.0, 2.0, N),
                    "rx", ms=6, label="closed")
        if alpha == 1.2:
            ax.axhline(0, color="k", lw=0.8)
        ax.set_title(title)
        ax.set_xlabel("n")
        ax.set_ylabel("$C_n$")
        ax.legend(fontsize=8)
    fig.suptitle("Linear model: $C_{n+1} = C_n - \\alpha\\beta C_{n-1} + m$  ($\\beta=m=1$, $C_0=C_1=2$)")
    fig.tight_layout()
    fig.savefig("Mod2\\fig1_linear.png", dpi=200)

def fig2(plot):
    fig = plot[0]
    for ax, (title, k) in zip(plot[1].flat, nl_cases):
        alpha = k**2 / (beta * m)
        Cs, Vs = steady_state(alpha, beta, m)
        C, V = iterate_nonlinear(alpha, beta, m, 1.1 * Cs, Vs, N)
        trajectories[k] = (C, V, Cs, Vs)
        ax.plot(range(N + 1), C, "o-", ms=4, label="$C_n$")
        ax.plot(range(N + 1), V, "s-", ms=4, label="$V_n$")
        ax.axhline(Cs, ls="--", color="C0", alpha=0.6, label=f"$C^*$ = {Cs:.2f}")
        ax.axhline(Vs, ls="--", color="C1", alpha=0.6, label=f"$V^*$ = {Vs:.2f}")
        ax.set_title(title)
        ax.set_xlabel("n")
        ax.legend(fontsize=8)
    fig.suptitle("Nonlinear model: $\\beta=m=1$, $C_0=1.1C^*$, $V_0=V^*$")
    fig.tight_layout()
    fig.savefig("Mod2\\fig2_nonlinear.png", dpi=200)

def fig3(plot, mods, ks):
    fig, ax = plot
    ax.plot(ks, mods, label="largest $|\\lambda|$")
    ax.axhline(1, ls="--", color="r", label="$|\\lambda|=1$")
    ax.axvline(3 - 2 * np.sqrt(2), ls=":", color="gray", label="$k=3-2\\sqrt{2}$")
    ax.set_xlabel("$k = \\sqrt{\\alpha\\beta m}$")
    ax.set_ylabel("largest eigenvalue")
    ax.set_title("Stability for nonlinear steady state")
    ax.legend()
    fig.tight_layout()
    fig.savefig("Mod2\\fig3_eigenvalues.png", dpi=200)

def fig4(plot):
    fig = plot[0]
    for ax, k in zip(plot[1], (0.5, 1.5)):
        C, V, Cs, Vs = trajectories[k]
        ax.plot(C, V, "o-", ms=3, lw=1)
        ax.plot(C[0], V[0], "go", label="start")
        ax.plot(Cs, Vs, "r*", ms=14, label="steady state")
        ax.set_xlabel("$C_n$")
        ax.set_ylabel("$V_n$")
        ax.set_title(f"k = {k}")
        ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig("Mod2\\fig4_phase.png", dpi=200)


def main():
    ks = np.linspace(0.01, 3, 600)
    mods = np.array([np.max(np.abs(np.roots([1, -(1 - k), k]))) for k in ks])

    fig1(plt.subplots(2, 2, figsize=(11, 7)))
    fig2(plt.subplots(2, 2, figsize=(11, 7)))
    fig3(plt.subplots(figsize=(7, 4.5)), mods, ks)
    fig4(plt.subplots(1, 2, figsize=(11, 4.5)))

    plt.show()

main()