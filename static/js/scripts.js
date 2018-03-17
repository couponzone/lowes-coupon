var myApp = angular.module('myApp', []);

function Main($scope, $http){
  $http.get('https://api.randomuser.me/0.4/?results=20').success(function(data) {
    $scope.users = data.results;
    
    $('#loader').hide();
    $('#userList').show();
  }).error(function(data, status) {
    alert('get data error!');
  });
  
  $scope.showDetail = function (u) {
    $scope.active = u;
  };
  
  $scope.doPost = function() {
  
    $http.get('http://api.randomuser.me/0.4/').success(function(data) {
      
      var newUser = data.results[0];
      newUser.user.text = $('#inputText').val();
      newUser.date = new Date();
      $scope.users.push(newUser);
    }).error(function(data, status) {
      alert('get data error!');
    });
  }

}

