(function(T){
T.CONFIG={
  PLAYER_MOVE_SPEED:200,      // px/giây - chỉnh tốc độ ở đây
  ANIM_WALK_FPS:10,           // FPS animation đi bộ
  ANIM_IDLE_FPS:5,            // idle thở nhẹ (4 frame); 0 = đứng yên
  ANIM_RUN_FPS:12,            // FPS animation chạy
  ANIM_JUMP_FPS:12,           // FPS animation nhảy (9 frame ~ 0.75s)
  ANIM_ATTACK_FPS:12,         // FPS animation chém (9 frame ~ 0.75s)
  PLAYER_RUN_SPEED_MULT:1.6,  // chạy nhanh gấp bao nhiêu lần đi bộ (giữ Shift / đẩy joystick hết cỡ)
  STICK_RUN_THRESHOLD:0.9,    // joystick đẩy quá mức này thì chạy
  PLAYER_SPRITE_SCALE:2,      // phải là số nguyên để pixel sắc nét (frame 64px -> 128px)
  CAMERA_FOLLOW_SPEED:14,     // càng cao càng bám sát
  CAMERA_TARGET_OFFSET_Y:-52, // nhắm vào thân người thay vì chân
  MAP_SCALE:3,                // phóng ảnh map x3 (số nguyên) cho khớp cỡ nhân vật
  MAP_SPAWN:{x:690,y:690},    // điểm xuất hiện (pixel trong ảnh gốc) - đường đất dưới giếng
  FRAME:{w:64,h:64,ax:32,ay:60}, // ô frame 64x64 + anchor giữa hai bàn chân (cố định cho mọi hướng)
};
})(window.Tutien=window.Tutien||{});
