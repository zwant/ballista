import datetime

import redis
from flask import Flask, g, render_template, request, redirect, url_for, jsonify, abort


app = Flask(__name__)
app.config.from_object('ballista.config')

redis = redis.StrictRedis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], db=app.config['REDIS_DB'])

@app.route('/package/<package_name>/', methods=['DELETE', 'POST'])
def update_package(package_name):
    if request.method == 'DELETE':
        _delete_package(package_name)
        return jsonify(result='SUCCESS')
    elif request.method == 'POST':
        form = UpdatePackageForm(request.form, csrf_enabled=False)
        if form.validate():
            _update_package_version(package_name, form.new_package_version.data)
            return redirect(url_for('start_page'))
    abort(400)


@app.route('/', methods=['GET', 'POST'])
def start_page():
    form = AddPackageForm(request.form, csrf_enabled=False)
    error_msg = None
    if request.method == 'POST' and form.validate():
        # Check that the package exists
        if utils.check_if_package_exists_on_pypi(form.package_name.data):
            g.db.execute('INSERT INTO watched_packages(package_name, package_version) VALUES (?,?)', [form.package_name.data, form.package_version.data])
            g.db.commit()
            return redirect(url_for('start_page'))
        else:
            error_msg = 'No such package found on PyPI'

    all_packages = query_db('SELECT * FROM watched_packages')

    for package in all_packages:
        # Check if we have a recent version already...
        max_age = ( datetime.datetime.now() - datetime.timedelta(hours=app.config['MAX_AGE_HOURS_BEFORE_UPDATE']))
        if not package['last_updated'] or \
           ( package['last_updated'] and
             package['last_updated'] <  max_age):
            # No recent version...
            pypi_package_info = utils.get_package_info_from_pypi(package['package_name'])
            if pypi_package_info:
                package['latest_version'] = pypi_package_info['version']
                package['package_url'] = pypi_package_info['package_url']
                g.db.execute('UPDATE watched_packages SET latest_version=?, last_updated=?, package_url=? WHERE package_name=?', [package['latest_version'],
                                                                                                                                  datetime.datetime.now(),
                                                                                                                                  package['package_url'],
                                                                                                                                  package['package_name']])
                g.db.commit()
        # Latest is newer than current
        if utils.compare_package_versions(package['latest_version'], package['package_version']):
            package['is_old'] = True
        else:
            package['is_old'] = False

    return render_template('start_page.html', form=form, all_packages=all_packages, error_msg=error_msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)