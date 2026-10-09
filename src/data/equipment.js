// Trang bị: mỗi món = 1 thư mục sheet cùng bố cục với base (8 hướng, idle + walk).
// Thêm đồ mới: bỏ sheet vào assets/player/<id>/ rồi khai báo ở ITEMS. Không cần sửa code animation.
(function(T){
T.EQUIP_SLOTS=['shoes','clothes','hair','weapon'];   // thứ tự vẽ từ dưới lên (base luôn vẽ trước)
T.ITEMS={
  hair_topknot:{slot:'hair',   name:'Búi tóc',  path:'player/hair_topknot'},
  robe_dao_bao:{slot:'clothes',name:'Đạo bào',  path:'player/robe_dao_bao'},
  shoes_cloth: {slot:'shoes',  name:'Giày vải', path:'player/shoes_cloth'},
  // anims: món chỉ có sheet cho một số animation (kiếm hiện chỉ hiện lúc chém; layer thiếu sheet sẽ bị bỏ qua)
  sword_purple:{slot:'weapon', name:'Kiếm tím',  path:'player/sword_purple', anims:['attack']},
  sword_gold:  {slot:'weapon', name:'Kiếm vàng', path:'player/sword_gold',   anims:['attack']},
  sword_fire:  {slot:'weapon', name:'Kiếm lửa',  path:'player/sword_fire',   anims:['attack']},
  sword_ice:   {slot:'weapon', name:'Kiếm băng', path:'player/sword_ice',    anims:['attack']},
  sword_jade:  {slot:'weapon', name:'Kiếm ngọc', path:'player/sword_jade',   anims:['attack']}
};
T.DEFAULT_EQUIP={hair:'hair_topknot',clothes:'robe_dao_bao',shoes:'shoes_cloth',weapon:'sword_purple'};
})(window.Tutien=window.Tutien||{});
