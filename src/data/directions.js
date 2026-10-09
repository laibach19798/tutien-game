// Sheet 8 hàng theo thứ tự PixelLab: south, south-east, east, north-east, north, north-west, west, south-west.
// Mỗi hướng có sprite riêng nên không cần lật ngang (flip:true nếu sau này muốn tiết kiệm sheet).
// Sai hướng thì sửa số row tại đây.
(function(T){
T.DIRECTIONS={
  DOWN:{row:0}, DOWN_RIGHT:{row:1}, RIGHT:{row:2}, UP_RIGHT:{row:3},
  UP:{row:4},   UP_LEFT:{row:5},    LEFT:{row:6},  DOWN_LEFT:{row:7}
};
const ORDER=['RIGHT','DOWN_RIGHT','DOWN','DOWN_LEFT','LEFT','UP_LEFT','UP','UP_RIGHT']; // theo góc, trục y hướng xuống
T.dirFromVector=(x,y)=>ORDER[(Math.round(Math.atan2(y,x)/(Math.PI/4))+8)%8]; // nhận cả vector tự do từ joystick
// Clip animation: sheet = tên file trong thư mục layer. Thêm RUN/ATTACK/CAST... tại đây
T.ANIMATIONS={
  WALK:{sheet:'walk',fpsKey:'ANIM_WALK_FPS'},
  IDLE:{sheet:'idle',fpsKey:'ANIM_IDLE_FPS'},
  RUN:{sheet:'run',fpsKey:'ANIM_RUN_FPS'},
  JUMP:{sheet:'jump',fpsKey:'ANIM_JUMP_FPS',loop:false}, // chạy 1 lần rồi dừng ở frame cuối
  ATTACK:{sheet:'attack',fpsKey:'ANIM_ATTACK_FPS',loop:false,frame:{w:96,h:96,ax:48,ay:76}} // ô lớn hơn để chứa vệt chém
};
})(window.Tutien=window.Tutien||{});
