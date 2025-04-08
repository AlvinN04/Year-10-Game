# Camera boundaries to prevent moving out of the level
    if camera_x > 0:
        camera_x = 0
    if camera_x < -level_width + width:
        camera_x = -level_width + width

    if camera_y > 0:
        camera_y = 0
    if camera_y < -level_height + height:
        camera_y = -level_height + height