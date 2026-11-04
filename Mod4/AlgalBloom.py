import numpy as np
import matplotlib.pyplot as plt

gamma = 0.01
qC = 2.0
delta = 0.05
eps = 0.4
a0 = 2.0
C0 = 4.0


def rhs(t, y, eta, gamma, qC, delta, eps):
    a, C = y
    return [eta * a - gamma * a**2,
            qC - delta * a - eps * C]

def euler(f, y0, t_end, n_steps, args):
    t = np.linspace(0, t_end, n_steps + 1)
    h = t[1] - t[0]
    y = np.zeros((n_steps + 1, len(y0)))
    y[0] = y0
    for i in range(n_steps):
        y[i + 1] = y[i] + h * np.array(f(t[i], y[i], *args))
    return t, y

def equilibria(eta, gamma, qC, delta, eps):
    eq1 = (0.0, qC / eps)
    eq2 = (eta / gamma, (qC - delta * eta / gamma) / eps)
    return eq1, eq2

def run_problem(label, alpha, beta, gamma, qC, delta, eps, a0, C0, t_end, fname):
    eta = alpha - beta
    t, y = euler(rhs, [a0, C0], t_end, 4000, (eta, gamma, qC, delta, eps))
    a, C = y[:, 0], y[:, 1]
    eq1, eq2 = equilibria(eta, gamma, qC, delta, eps)

    print(f"{label}: eta = {eta:.3f}")
    print(f"  Equilibrium 1 (a*, C*) = ({eq1[0]:.3f}, {eq1[1]:.3f})")
    print(f"  Equilibrium 2 (a*, C*) = ({eq2[0]:.3f}, {eq2[1]:.3f})")
    print(f"  Final state at t = {t_end}: a = {a[-1]:.4f}, C = {C[-1]:.4f}")

    fig, ax1 = plt.subplots(figsize=(7, 4.5))
    ax1.plot(t, a, color="tab:green", label="a(t), algae")
    ax1.set_xlabel("Time (days)")
    ax1.set_ylabel("Algae density a(t) (µg/L)", color="tab:green")
    ax2 = ax1.twinx()
    ax2.plot(t, C, color="tab:blue", label="C(t), dissolved oxygen")
    ax2.set_ylabel("Dissolved oxygen C(t) (mg/L)", color="tab:blue")
    ax1.set_title(f"{label}: a(t) and C(t) versus time (η = {eta:.2f})")
    lines = ax1.get_lines() + ax2.get_lines()
    ax1.legend(lines, [l.get_label() for l in lines], loc="best")
    fig.tight_layout()
    fig.savefig(f"Mod3\\{fname}_time.png", dpi=200)

    fig, ax = plt.subplots(figsize=(6.5, 5))
    ax.plot(a, C, color="tab:purple", label="Trajectory")
    ax.plot(a0, C0, "ko", markersize=8, label=f"Initial condition ({a0}, {C0})")
    ax.plot(*eq1, "r*", markersize=14, label=f"Equilibrium 1 ({eq1[0]:.2f}, {eq1[1]:.2f})")
    if label.startswith("Problem 2"):
        ax.plot(*eq2, "g^", markersize=10, label=f"Equilibrium 2 ({eq2[0]:.2f}, {eq2[1]:.2f})")
    ax.set_xlabel("Algae density a (µg/L)")
    ax.set_ylabel("Dissolved oxygen C (mg/L)")
    ax.set_title(f"{label}: phase plot of C versus a")
    ax.legend(loc="best")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(f"Mod3\\{fname}_phase.png", dpi=200)


def main():
    # Problem 1: nat grow rate < 0  (alpha = 0.3, beta = 0.5 -> -0.2)
    run_problem("Problem 1", alpha=0.3, beta=0.5, gamma=gamma, qC=qC,
                delta=delta, eps=eps, a0=a0, C0=C0, t_end=40, fname="problem1")
    
    # Problem 2: nat grow rate > 0  (alpha = 0.5, beta = 0.2 -> 0.3)
    run_problem("Problem 2", alpha=0.5, beta=0.2, gamma=gamma, qC=qC,
                delta=delta, eps=eps, a0=a0, C0=C0, t_end=40, fname="problem2")
    
    plt.show()


main()