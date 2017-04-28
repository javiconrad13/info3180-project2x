/*global angular*/
var app = angular.module("Wishlist",['ui.bootstrap']);


app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
  });

app.controller('NewItemCtrl', function($scope, $http, $uibModal){
    $scope.item_url = "";
    $scope.img_url = "";
    $scope.selectedimg = "";

    $scope.prod_url = "";
    $scope.images = [];
    $scope.params= ["Test", "*", "Test2"];

    $scope.get_thumbs = function(){
        if($scope.prod_url == ""){
            alert("No url entered.");
        } else {
            var base = "http://info3180-project2-drellimal2-1.c9users.io:8080/";
            var route = "/api/thumbnail/process?url=";
            var data_url = route + $scope.prod_url;
            
            for(var x = 0; x < 4;x++){
                $http.get(data_url).success(function(data){
                    console.log(data);
                    if (data.data != {}){
                        $scope.images = data.data.thumbails;
                    }
                });
            }

            console.log($scope.images);
        }
      
    };
    
    $scope.search= function(){
          // $scope.get_thumbs();
          $scope.open();
   
    };
    $scope.open = function (size) {

    $scope.animationsEnabled = true;
    var modalInstance = $uibModal.open({
      animation: $scope.animationsEnabled,
      templateUrl: 'myModalContent.html',
      controller: 'ThumbnailCtrl',
      resolve: {
          prod_url: function () {
          return $scope.prod_url;
        }

        }
      
    });
    
    modalInstance.result.then(function (img) {
      $scope.img_url = img;
      $scope.selectedimg = img;
    }, function () { 
      
    });
    
    };
});

app.controller('ThumbnailCtrl', function ($scope, $http, $uibModalInstance, prod_url) {

  $scope.images = [];
  $scope.prod_url = prod_url;

    $scope.get_thumbs = function(){
        if($scope.prod_url == ""){
            alert("No url entered.");
        } else {
            var base = "http://info3180-project2-wushum.c9users.io:8080/";
            var route = "/api/thumbnail/?url=";
            var data_url = route + $scope.prod_url;
            console.log(data_url);
            console.log(data_url);
            for(var x = 0; x < 1;x++){
                $http.get(data_url).success(function(data){
                    console.log(data);
                    if (data.data != {}){
                        $scope.images = data.data.thumbails;
                    }
                });
            }

            console.log($scope.images);
        }
      
    };
    
  $scope.get_thumbs();
  $scope.selected = "";

  $scope.selectimg = function(imgurl){
    $scope.selected = imgurl;
    console.log(imgurl);
    console.log($scope.selected);
  };
  $scope.ok = function () {
    if($scope.selected == ""){
      alert("Please choose an image");
    }else{
  
      $uibModalInstance.close($scope.selected);
    }
  };

  $scope.cancel = function () {
    $uibModalInstance.dismiss('cancel');
  };
});
