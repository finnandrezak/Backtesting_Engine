import matplotlib.pyplot as plt
"""
Visualizer: plots the equity curve of the strategy and compares it to a benchmark. 
Shows performance metrics in a text box
"""
class Visualizer:
    @staticmethod
    def plot_results(equity_curve, stats, benchmark_curve=None):
        if not equity_curve:
            print("Visualizer: No data to plot")
            return

        times, values = zip(*equity_curve)

        plt.figure(figsize=(12, 7))
        plt.plot(times, values, label='Strategy Equity', color='#007bff', linewidth=2)

        if benchmark_curve:
            b_times, b_values =zip(*benchmark_curve)
            plt.plot(b_times, b_values, label='Benchmark Equity', color='#ff7f0e', linestyle='--',
                     alpha=0.8, linewidth=1.6)

        #creating metrics box
        stats_text = (
            f"Initial Capital: {stats['initial']:.2f} $\n"
            f"Final Equity: {stats['final']:.2f} $\n"
            f"Total Return: {stats['return_pct']:.2f} %\n"
            f"Benchmark Return: {stats['benchmark_return']:.2f} %\n"
            f"Max Drawdown: {stats['max_drawdown']:.2f} %"
        )
        #positioning metrics box
        plt.gca().text(0.02, 0.95, stats_text, transform = plt.gca().transAxes,
                       fontsize=10, verticalalignment='top',
                       bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='#cccccc'))


        plt.title('Backtest results: Equity Curve with Benchmark', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Date / Time', fontsize=12)
        plt.ylabel('Capital in $', fontsize=12)
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.legend(loc='upper right', frameon=True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.show()