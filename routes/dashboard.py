from flask import Blueprint, render_template
from services.auth import auth_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@auth_required
def dashboard():
    return render_template('dashboard.html')