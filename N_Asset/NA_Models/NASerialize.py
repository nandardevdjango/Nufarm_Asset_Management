from rest_framework import serializers

from .models import NAGoodsLost,NAGoodsLending,NAGoodsOutwards
class NAGoodsLostSerializer(serializers.ModelSerializer):
    class Meta:
        model = NAGoodsLost
        fields = '__all__'
class NAGoodsOutWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NAGoodsOutwards
        fields =  '__all__'
class NAGoodLendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = NAGoodsLending
        fields =  '__all__'