#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

results = {
    'stats': None,
    'equity_curve': [],
    'trades': [],
    'benchmark': []
}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/backtest', methods=['POST'])
def backtest():
    try:
        global results
        results = {
            'stats': None,
            'equity_curve': [],
            'trades': [],
            'benchmark': []
        }
        
        config = request.json or {}
        print(f"Starting backtest with config: {config}")
        
        default_config = {
            'tickers': ['SPY'],
            'start': '2020-01-01',
            'end': '2021-01-01',
            'interval': '1d',
            'capital': 1000000.0,
            'stop_loss': 0.2,
            'risk_per_trade_pct': 0.5,
            'strategy': 'SMA_Strategy'
        }
        default_config.update(config)
        
        strategy_name = default_config.get('strategy', 'SMA_Strategy')
        print(f"Strategy selected: {strategy_name}")
        
        if strategy_name == 'SMA_Strategy':
            from strategy.SMA_Strategy import SMA_Strategy
            default_config['strategy_class'] = SMA_Strategy
        elif strategy_name == 'Advanced_Volatility_Strategy':
            from strategy.Advanced_Volatility_Strategy import Advanced_Volatility_Strategy
            default_config['strategy_class'] = Advanced_Volatility_Strategy
        elif strategy_name == 'Regime_Switch_Strategy':
            from strategy.Regime_Switch_Strategy import Regime_Switch_Strategy
            default_config['strategy_class'] = Regime_Switch_Strategy
        elif strategy_name == 'SimpleStrategy':
            from strategy.SimpleStrategy import SimpleStrategy
            default_config['strategy_class'] = SimpleStrategy
        else:
            from strategy.SMA_Strategy import SMA_Strategy
            default_config['strategy_class'] = SMA_Strategy
        
        from main import run_backtest
        portfolio, stats, benchmark = run_backtest(default_config, show_plot=False)
        
        results['stats'] = stats
        results['equity_curve'] = portfolio.get_equity_curve_data()
        results['trades'] = portfolio.get_trades_data()
        
        try:
            benchmark_curve = benchmark.get_curve()
            results['benchmark'] = [{'timestamp': str(ts), 'value': float(val)} for ts, val in benchmark_curve]
        except Exception as e:
            print(f"Benchmark error: {e}")
            results['benchmark'] = []
        
        return jsonify({'success': True, 'stats': stats}), 200
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/results', methods=['GET'])
def get_results():
    return jsonify({
        'stats': results['stats'],
        'equity_curve': results['equity_curve'],
        'trades': results['trades'],
        'benchmark': results['benchmark']
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify(results['stats'] or {})

@app.route('/api/equity-curve', methods=['GET'])
def get_equity():
    return jsonify(results['equity_curve'] or [])

@app.route('/api/trades', methods=['GET'])
def get_trades():
    return jsonify(results['trades'] or [])

@app.route('/', methods=['GET'])
def serve_dashboard():
    return send_file('dashboard.html', mimetype='text/html')

if __name__ == '__main__':
    print("\nAPI Server starting on http://localhost:5001\n")
    app.run(debug=False, port=5001, use_reloader=False)

