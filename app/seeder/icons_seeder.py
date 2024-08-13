from app.extensions.db import db
from app.schema.Master import Icon
import os

def add_icons_to_db(app):
    icon_dir = os.path.join(app.root_path, 'static', 'icons')
    allowed_extensions = ['.png', '.svg']  # Add more extensions as needed
    for filename in os.listdir(icon_dir):
        if any(filename.endswith(ext) for ext in allowed_extensions):
            # Convert filename to lowercase and replace spaces with hyphens
            new_filename = filename.lower().replace(' ', '-')
            
            existing_icon = Icon.query.filter_by(filename=new_filename).first()
            if existing_icon is None:
                icon_path = os.path.join('static', 'icons', new_filename)
                new_icon = Icon(filename=new_filename, file_path=icon_path)
                db.session.add(new_icon)
    db.session.commit()
