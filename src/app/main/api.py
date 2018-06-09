"""
Interviews management API.
"""
from flask import jsonify

from . import main


@main.route('/api/v1/echo', methods=['GET'])
def echo():
    """Dummy endpoint to test app's setup."""
    return jsonify({'success': True})
