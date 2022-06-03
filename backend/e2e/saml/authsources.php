
<?php

$config = array(

    'admin' => array(
        'core:AdminPassword',
    ),

    'example-userpass' => array(
        'exampleauth:UserPass',
        'user1@gilead.com:user1pass' => array(
            'surName' => 'Tyler',
            'givenName' => 'Durden',
            'email' => 'user1@gilead.com',
        ),
        'user2@gilead.com:user2pass' => array(
            'surName' => 'Charlie',
            'givenName' => 'Brown',
            'email' => 'user2@gilead.com',
        ),
    ),

);
