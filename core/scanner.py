import os


class DirectoryScanner:
    """Escanea directorios y genera árbol ASCII."""

    def __init__(self, config_manager):
        self.config = config_manager

    def scan(self, root_dir, omit_images=False):
        """
        Escanea el directorio raíz y retorna el árbol ASCII completo.

        Args:
            root_dir: Ruta del directorio a escanear.
            omit_images: Si True, omite archivos de imagen.

        Returns:
            String con el árbol ASCII.

        Raises:
            ValueError: Si la ruta no es un directorio válido.
        """
        if not os.path.isdir(root_dir):
            raise ValueError(f"'{root_dir}' no es un directorio válido.")

        project_name = os.path.basename(os.path.normpath(root_dir))
        header = f"{project_name}/\n"
        tree = self._build_tree(root_dir, omit_images, prefix='', depth=0)

        return header + tree

    def _build_tree(self, directory, omit_images, prefix, depth):
        """Construye recursivamente el árbol ASCII."""
        max_depth = self.config.max_depth

        if max_depth != -1 and depth >= max_depth:
            return ''

        result = ''
        entries = self._get_filtered_entries(directory, omit_images)
        folders = entries['folders']
        files = entries['files']

        total_folders = len(folders)
        total_files = len(files)
        total = total_folders + total_files

        # Procesar carpetas
        for i, folder_name in enumerate(folders):
            folder_path = os.path.join(directory, folder_name)
            is_last = (i == total_folders - 1) and (total_files == 0)
            connector = '└── ' if is_last else '├── '
            extension = '    ' if is_last else '│   '

            result += f"{prefix}{connector}📁 {folder_name}/\n"
            result += self._build_tree(
                folder_path, omit_images,
                prefix + extension, depth + 1
            )

        # Procesar archivos
        for i, file_name in enumerate(files):
            is_last = (i == total_files - 1)
            connector = '└── ' if is_last else '├── '
            icon = self._get_file_icon(file_name)

            result += f"{prefix}{connector}{icon} {file_name}\n"

        return result

    def _get_filtered_entries(self, directory, omit_images):
        """Filtra y clasifica entradas del directorio."""
        try:
            entries = sorted(os.listdir(directory))
        except PermissionError:
            return {'folders': [], 'files': []}

        ignored_folders = self.config.ignored_folders
        ignored_files = self.config.ignored_files
        ignored_extensions = self.config.ignored_extensions
        image_extensions = self.config.image_extensions
        show_hidden = self.config.show_hidden

        folders = []
        files = []

        for entry in entries:
            full_path = os.path.join(directory, entry)

            # Ocultar archivos/carpetas ocultos
            if not show_hidden and entry.startswith('.'):
                continue

            if os.path.isdir(full_path):
                if entry not in ignored_folders:
                    folders.append(entry)

            elif os.path.isfile(full_path):
                # Ignorar por nombre
                if entry in ignored_files:
                    continue

                # Ignorar por extensión
                _, ext = os.path.splitext(entry)
                ext = ext.lower()

                if ext in ignored_extensions:
                    continue

                # Omitir imágenes si corresponde
                if omit_images and ext in image_extensions:
                    continue

                files.append(entry)

        return {'folders': folders, 'files': files}

    def _get_file_icon(self, filename):
        """Retorna un emoji según la extensión del archivo."""
        _, ext = os.path.splitext(filename)
        ext = ext.lower()

        icon_map = {
            '.py': '🐍',
            '.js': '🟨',
            '.jsx': '⚛️',
            '.ts': '🔷',
            '.tsx': '⚛️',
            '.html': '🌐',
            '.css': '🎨',
            '.json': '📋',
            '.md': '📝',
            '.txt': '📄',
            '.yml': '⚙️',
            '.yaml': '⚙️',
            '.toml': '⚙️',
            '.ini': '⚙️',
            '.cfg': '⚙️',
            '.env': '🔐',
            '.sql': '🗃️',
            '.sh': '🐚',
            '.bat': '🖥️',
            '.cmd': '🖥️',
            '.xml': '📰',
            '.svg': '🖼️',
            '.png': '🖼️',
            '.jpg': '🖼️',
            '.gif': '🖼️',
            '.ico': '🖼️',
            '.mp3': '🎵',
            '.mp4': '🎬',
            '.zip': '📦',
            '.rar': '📦',
            '.gz': '📦',
            '.tar': '📦',
            '.pdf': '📕',
            '.doc': '📘',
            '.docx': '📘',
            '.xls': '📊',
            '.xlsx': '📊',
            '.lock': '🔒',
            '.gitignore': '🚫',
        }

        # Casos especiales por nombre
        name_map = {
            'Dockerfile': '🐳',
            'docker-compose.yml': '🐳',
            'Makefile': '🔧',
            'LICENSE': '📜',
            'README.md': '📖',
        }

        if filename in name_map:
            return name_map[filename]

        return icon_map.get(ext, '📄')
