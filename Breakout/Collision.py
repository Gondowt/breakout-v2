import abc

class CollisionContext:
    def setCollisionStrategy(self, strategy):
        self.strategy = strategy

    def checkCollision(self, ball, objectCollision):
        self.strategy.collision(ball, objectCollision)

class CollisionStrategy:
    __metaclass__=abc.ABCMeta

    @abc.abstractmethod
    def collision(self, ball, objectCollision):
        return


class BallBricksCollision(CollisionStrategy):
    def collision(self, ball, objectCollision):
        bricks = objectCollision.bricks
        for i in range(len(bricks)) :
            if (ball.y + 2*ball.radius > bricks[i].y and ball.y < bricks[i].y + bricks[i].sizeh) and (ball.x + 2*ball.radius > bricks[i].x and ball.x < bricks[i].x + bricks[i].sizew):
                #check if the ball is in the brick.
                if (ball.x + ball.radius > bricks[i].x and ball.x + ball.radius < bricks[i].x + bricks[i].sizew) and (ball.y + ball.radius < bricks[i].y or ball.y + ball.radius > bricks[i].y+bricks[i].sizeh):
                    #check if the ball is under or on the brick.
                    if ball.last_iteration == False:
                        #check if the ball was already in the brick at the last iteration.
                        ball.speedy *=-1
                        objectCollision.change_score(bricks[i].life, ball)
                        bricks[i].life -=1
                    ball.last_iteration = True
                    #replace the ball outside of the brick.
                    if ball.y + ball.radius < bricks[i].y :
                        ball.y = bricks[i].y - 2*ball.radius
                    else :
                        ball.y = bricks[i].y + bricks[i].sizeh
                elif (ball.y + ball.radius > bricks[i].y and ball.y + ball.radius < bricks[i].y + bricks[i].sizeh) and (ball.x + ball.radius < bricks[i].x or ball.x + ball.radius > bricks[i].x+bricks[i].sizew):
                    #check if the ball is at the left or at the right of the brick.
                    if ball.last_iteration == False:
                        #check if the ball was already in the brick at the last iteration.
                        ball.speedx *=-1
                        objectCollision.change_score(bricks[i].life, ball)
                        bricks[i].life -=1
                    ball.last_iteration = True
                    #replace the ball outside of the brick.
                    if ball.x + ball.radius < bricks[i].x :
                        ball.x = bricks[i].x - 2*ball.radius
                    else :
                        ball.x = bricks[i].x + bricks[i].sizew
                else :
                    #check if the brick is in a corner.
                    if ball.last_iteration == False:
                        #check if the ball was already in the brick at the last iteration.
                        objectCollision.change_score(bricks[i].life, ball)
                        bricks[i].life -=1
                        if (ball.speedx > 0 and ball.x + ball.radius < bricks[i].x) or (ball.speedx < 0 and ball.x + ball.radius > bricks[i].x+bricks[i].sizeh):
                            ball.speedx *=-1
                        if (ball.speedy > 0 and ball.y + ball.radius < bricks[i].y) or (ball.speedy < 0 and ball.y + ball.radius > bricks[i].y+bricks[i].sizeh):
                            ball.speedy *=-1
                    ball.last_iteration = True
                    #replace the ball outside of the brick.
            else:
                bricks[i].last_iteration = False

class BallPaddleCollision(CollisionStrategy):
    def collision(self, ball, objectCollision):
        #Check the collisions between the ball and the paddle.
        if (ball.y + 2*ball.radius > objectCollision.y and ball.y < objectCollision.y + objectCollision.sizeh) and (ball.x + 2*ball.radius > objectCollision.x and ball.x < objectCollision.x + objectCollision.sizew):
            #check if the ball is in the paddle.
            if (ball.x + ball.radius > objectCollision.x and ball.x + ball.radius < objectCollision.x + objectCollision.sizew) and (ball.y + ball.radius < objectCollision.y or ball.y + ball.radius > objectCollision.y+objectCollision.sizeh):
                #check if the ball is under or on the paddle.
                if ball.last_iteration == False:
                    #check if the ball was already in the paddle at the last iteration.
                    ball.speedy *=-1
                    #call the function to compute the rebound of the ball.
                    ball.rebound_paddle(objectCollision)
                    ball.rebound_number +=1
                ball.last_iteration = True
                #replace the ball outside of the paddle.
                if ball.y + ball.radius < objectCollision.y :
                    ball.y = objectCollision.y - 2*ball.radius
                else :
                    ball.y = objectCollision.y + objectCollision.sizeh
            elif (ball.y + ball.radius > objectCollision.y and ball.y + ball.radius < objectCollision.y + objectCollision.sizeh) and (ball.x + ball.radius < objectCollision.x or ball.x + ball.radius > objectCollision.x+objectCollision.sizew):
                #check if the ball is at the left or at the right of the paddle.
                if ball.last_iteration == False:
                    #check if the ball was already in the paddle at the last iteration.
                    ball.speedx *=-1
                    ball.rebound_number +=1
                ball.last_iteration = True
                #replace the ball outside of the paddle.
                if ball.x + ball.radius < objectCollision.x :
                    ball.x = objectCollision.x - 2*ball.radius
                else :
                    ball.x = objectCollision.x + objectCollision.sizew
            else :
                #check if the paddle is in a corner.
                if ball.last_iteration == False:
                    #check if the ball was already in the paddle at the last iteration.
                    ball.rebound_paddle(objectCollision)
                    if (ball.speedy > 0 and ball.y + ball.radius < objectCollision.y) or (ball.speedy < 0 and ball.y + ball.radius > objectCollision.y+objectCollision.sizeh):
                        ball.speedy *=-1
                    ball.rebound_number +=1
                ball.last_iteration = True
                #replace the ball outside of the paddle.
        else:
            ball.last_iteration = False

class BallWindowCollision(CollisionStrategy):
    def collision(self, ball, objectCollision):
        if ball.x < 0 or ball.x > 800-2*ball.radius:
            if ball.x < 0 : ball.x = 0
            elif ball.x > 800-2*ball.radius : ball.x = 800-2*ball.radius
            ball.speedx *=-1
        if ball.y < 0 or ball.y > 650:
            if ball.y < 0 : ball.y = 0
            elif ball.y > 650: ball.game_over = True
            ball.speedy *=-1
