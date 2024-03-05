import face_recognition


def face(image_path, known_faces, known_names):
    unknown_image = face_recognition.load_image_file(image_path)
    unknown_face_locations = face_recognition.face_locations(unknown_image)

    if not unknown_face_locations:
        name = "Unknown"
        print(f"Name: {name}")
        print("\n")
        return name

    unknown_face_encodings = face_recognition.face_encodings(unknown_image, unknown_face_locations)

    for face_encoding in unknown_face_encodings:
        matches = []

        for known_face, known_name in zip(known_faces, known_names):
            result = face_recognition.compare_faces([known_face], face_encoding)

            if result[0]:
                matches.append((known_name, result))

        if len(matches) > 0:
            matches.sort(key=lambda x: x[1][0], reverse=True)
            name = matches[0][0]

        else:
            name = "Unknown"

        print(f"Name: {name}")
        print("\n")
        return name
