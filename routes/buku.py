
from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_db

bp = Blueprint('buku', __name__, url_prefix='/buku')


# =========================
# MENAMPILKAN DAFTAR BUKU
# =========================
@bp.route('/')
def index():
    db = get_db()

    keyword = request.args.get('keyword', '')

    with db.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM buku
            WHERE judul LIKE %s OR pengarang LIKE %s
            ORDER BY id_buku
        """, (f'%{keyword}%', f'%{keyword}%'))

        data = cursor.fetchall()

    return render_template(
        'buku/index.html',
        buku=data,
        keyword=keyword
    )


# =========================
# TAMBAH BUKU
# =========================
@bp.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        db = get_db()

        id_buku = request.form.get('id_buku', '').strip()
        judul = request.form.get('judul', '').strip()
        pengarang = request.form.get('pengarang', '').strip()
        penerbit = request.form.get('penerbit', '').strip()
        tahun = request.form.get('tahun_terbit', '').strip() or None
        stok = request.form.get('stok', '0').strip()

        if not id_buku or not judul or not pengarang:
            flash('ID, judul dan pengarang wajib diisi.')
            return redirect(url_for('buku.tambah'))

        try:
            stok = int(stok)

            if stok < 0:
                flash('Stok tidak boleh negatif.')
                return redirect(url_for('buku.tambah'))

            with db.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO buku
                    (id_buku, judul, pengarang, penerbit, tahun_terbit, stok)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    id_buku,
                    judul,
                    pengarang,
                    penerbit or None,
                    tahun,
                    stok
                ))

            db.commit()
            flash('Buku berhasil ditambahkan.')

        except Exception as e:
            db.rollback()
            print("ERROR TAMBAH BUKU:", repr(e))
            flash(f'Gagal menambahkan buku: {e}')

        return redirect(url_for('buku.index'))

    return render_template('buku/form.html', mode='tambah')


# =========================
# EDIT BUKU
# =========================
@bp.route('/edit/<id_buku>', methods=['GET', 'POST'])
def edit(id_buku):
    db = get_db()

    with db.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM buku WHERE id_buku = %s",
            (id_buku,)
        )
        data = cursor.fetchone()

    if not data:
        flash('Data buku tidak ditemukan.')
        return redirect(url_for('buku.index'))

    if request.method == 'POST':
        judul = request.form['judul'].strip()
        pengarang = request.form['pengarang'].strip()
        penerbit = request.form['penerbit'].strip()
        tahun = request.form['tahun_terbit'] or None
        stok = request.form['stok']

        try:
            stok = int(stok)

            if stok < 0:
                flash('Stok tidak boleh negatif.')
                return redirect(url_for('buku.edit', id_buku=id_buku))

            with db.cursor() as cursor:
                cursor.execute("""
                    UPDATE buku
                    SET judul=%s,
                        pengarang=%s,
                        penerbit=%s,
                        tahun_terbit=%s,
                        stok=%s
                    WHERE id_buku=%s
                """, (
                    judul,
                    pengarang,
                    penerbit or None,
                    tahun,
                    stok,
                    id_buku
                ))

            db.commit()
            flash('Buku berhasil diperbarui.')

        except Exception as e:
            db.rollback()
            print("ERROR EDIT BUKU:", repr(e))
            flash(f'Gagal memperbarui buku: {e}')

        return redirect(url_for('buku.index'))

    return render_template(
        'buku/form.html',
        mode='edit',
        data=data
    )

# =========================
# HAPUS BUKU
# =========================
@bp.route('/hapus/<id_buku>', methods=['GET', 'POST'])
def hapus(id_buku):
    db = get_db()

    try:
        with db.cursor() as cursor:
            cursor.execute(
                "DELETE FROM buku WHERE id_buku = %s",
                (id_buku,)
            )

            if cursor.rowcount == 0:
                flash('Data buku tidak ditemukan.')
            else:
                db.commit()
                flash('Buku berhasil dihapus.')

    except Exception as e:
        db.rollback()
        print("ERROR HAPUS BUKU:", repr(e))
        flash(f'Gagal menghapus buku: {e}')

    return redirect(url_for('buku.index'))
